"""
A few non-business data resource end points
"""

import json
import mimetypes
from functools import wraps
from itertools import groupby
from typing import Any, Callable, Dict, List, Optional, Union
from uuid import uuid4
import traceback

from django import http
from django.conf import settings
from django.db import IntegrityError, router, transaction, connection, models
from specifyweb.notifications.models import Message, Spmerging
from django.db.models import Q
from django.db.models.deletion import Collector
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.db.models.deletion import ProtectedError

from specifyweb.businessrules.exceptions import BusinessRuleException
from specifyweb.permissions.permissions import PermissionTarget, \
    PermissionTargetAction, PermissionsException, check_permission_targets, table_permissions_checker
from specifyweb.celery_tasks import LogErrorsTask, app
from . import api, models as spmodels
from .api import uri_for_model
from .build_models import orderings
from .load_datamodel import Table, FieldDoesNotExistError
from .specify_jar import specify_jar
from celery.utils.log import get_task_logger # type: ignore
logger = get_task_logger(__name__)

def login_maybe_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return http.HttpResponseForbidden()
        return view(request, *args, **kwargs)
    return wrapped

if settings.ANONYMOUS_USER:
    login_maybe_required = lambda func: func


class HttpResponseConflict(http.HttpResponse):
    status_code = 409

def openapi(schema, components={}):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            return view(*args, **kwargs)
        setattr(wrapped, '__schema__', {
            'schema': schema,
            'components': components
        })
        return wrapped
    return decorator

def api_view(dispatch_func):
    """Create a Django view function that handles exceptions arising
    in the api logic."""
    @login_maybe_required
    @cache_control(private=True, max_age=2)
    def view(request, *args, **kwargs):
        """RESTful API endpoint for most Specify datamodel resources.
        <model> is the table from the Specify datamodel. <id> is the
        row id.
        """
        try:
            return dispatch_func(request, *args, **kwargs)
        except api.StaleObjectException as e:
            return HttpResponseConflict(e)
        except api.MissingVersionException as e:
            return http.HttpResponseBadRequest(e)
        except http.Http404 as e:
            return http.HttpResponseNotFound(e)
    return view

resource = api_view(api.resource_dispatch)
collection = api_view(api.collection_dispatch)

def raise_error(request):
    """This endpoint intentionally throws an error in the server for
    testing purposes.
    """
    raise Exception('This error is a test. You may now return to your regularly '
                    'scheduled hacking.')

@login_maybe_required
@require_http_methods(['GET', 'HEAD'])
def delete_blockers(request, model, id):
    """Returns a JSON list of fields on <model> that point to related
    resources which prevent the resource <id> of that model from being
    deleted.
    """
    obj = api.get_object_or_404(model, id=int(id))
    using = router.db_for_write(obj.__class__, instance=obj)
    collector = Collector(using=using)
    collector.delete_blockers = []
    collector.collect([obj])
    result = flatten([
        [
            {
                'table': sub_objs[0].__class__.__name__,
                'field': field.name,
                'ids': [sub_obj.id for sub_obj in sub_objs]
            }
        ] for field, sub_objs in collector.delete_blockers
    ])
    return http.HttpResponse(api.toJson(result), content_type='application/json')

def flatten(l):
    return [item for sublist in l for item in sublist]

@login_maybe_required
@require_http_methods(['GET', 'HEAD'])
def rows(request, model):
    "Returns tuples from the table for <model>."
    return api.rows(request, model)

@require_http_methods(['GET', 'HEAD'])
@cache_control(max_age=365 * 24 * 60 * 60, public=True)
def images(request, path):
    """Returns images and icons from the Specify thickclient jar file
    under edu/ku/brc/specify/images/."""
    mimetype = mimetypes.guess_type(path)[0]
    path = 'edu/ku/brc/specify/images/' + path
    try:
        image = specify_jar.read(path)
    except KeyError as e:
        raise http.Http404(e)
    return http.HttpResponse(image, content_type=mimetype)

@login_maybe_required
@require_http_methods(['GET', 'HEAD'])
@cache_control(max_age=24 * 60 * 60, public=True)
def properties(request, name):
    """Returns the <name>.properities file from the thickclient jar file."""
    path = name + '.properties'
    return http.HttpResponse(specify_jar.read(path), content_type='text/plain')

class SetPasswordPT(PermissionTarget):
    resource = '/admin/user/password'
    update = PermissionTargetAction()

@openapi(schema={
    'post': {
        "requestBody": {
            "required": True,
            "description": "New user's password",
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "password": {
                                "type": "string",
                                "description": "New user's password",
                            },
                        },
                        'required': ['password'],
                        'additionalProperties': False
                    }
                }
            }
        },
        "responses": {
            "204": {"description": "Success",},
            "403": {"description": "Logged in user is not an admin."}
        }
    },
})
@login_maybe_required
@require_POST
def set_password(request, userid):
    """Set <userid> specify user's password to the value in the 'password'
    POST parameter.
    """
    check_permission_targets(None, request.specify_user.id, [SetPasswordPT.update])
    user = spmodels.Specifyuser.objects.get(pk=userid)
    user.set_password(request.POST['password'])
    user.save()
    return http.HttpResponse('', status=204)

class SetAgentsException(PermissionsException):
    status_code = 400

    def to_json(self):
        return {self.__class__.__name__: self.args[0]}

class AgentInUseException(SetAgentsException):
    "One of the agents being assigned is already assigned to another user."
    pass

class MultipleAgentsException(SetAgentsException):
    "Attempting to assign more than one agent per division to the user."
    pass

class MissingAgentForAccessibleCollection(SetAgentsException):
    "The user has access to a collection in a division that is not represented by any agent."
    pass

class SetUserAgentsPT(PermissionTarget):
    resource = '/admin/user/agents'
    update = PermissionTargetAction()

@openapi(schema={
    'post': {
        "requestBody": {
            "required": True,
            "description": "The list of agents to assign to the user represented by their ids.",
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "The agent ids."
                    }
                }
            }
        },
        "responses": {
            "204": {"description": "Success",},
            "400": {
                "description": "The request was rejected.",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "description": "The error.",
                            "properties": {
                                AgentInUseException.__name__: {
                                    'type': 'array',
                                    'description': AgentInUseException.__doc__,
                                    'items': {'type': 'integer'},
                                },
                                MultipleAgentsException.__name__: {
                                    'type': 'array',
                                    'description': MultipleAgentsException.__doc__,
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'divisionid': {'type': 'number'},
                                            'agentid1': {'type': 'number'},
                                            'agentid2': {'type': 'number'},
                                        },
                                    },
                                },
                                MissingAgentForAccessibleCollection.__name__: {
                                    'type': 'object',
                                    'description': MissingAgentForAccessibleCollection.__doc__,
                                    'properties': {
                                        'all_accessible_divisions': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'number',
                                                'description': 'Division ID',
                                            },
                                        },
                                        'missing_for_6': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'number',
                                                'description': 'Division ID',
                                            },
                                        },
                                        'missing_for_7': {
                                            'type': 'array',
                                            'items': {
                                                'type': 'number',
                                                'description': 'Division ID',
                                            },
                                        },
                                    },
                                }
                            }
                        }
                    }
                }
            }
        }
    },
})
@login_maybe_required
@require_POST
def set_user_agents(request, userid: int):
    "Sets the agents to represent the user in different disciplines."
    user = spmodels.Specifyuser.objects.get(pk=userid)
    new_agentids = json.loads(request.body)
    cursor = connection.cursor()

    with transaction.atomic():
        # clear user's existing agents
        spmodels.Agent.objects.filter(specifyuser_id=userid).update(specifyuser_id=None)

        # check if any of the agents to be assigned are used by other users
        in_use = spmodels.Agent.objects.select_for_update().filter(pk__in=new_agentids, specifyuser_id__isnull=False)
        if in_use:
            raise AgentInUseException([a.id for a in in_use])

        # assign the new agents
        spmodels.Agent.objects.filter(pk__in=new_agentids).update(specifyuser_id=userid)

        # check for multiple agents assigned to the user
        cursor.execute(
            """select divisionid, a1.agentid, a2.agentid
            from agent a1 join agent a2 using (specifyuserid, divisionid)
            where a1.agentid < a2.agentid and specifyuserid = %s
            """, [userid]
        )

        multiple = [
            {'divisonid': divisonid, 'agentid1': agentid1, 'agentid2': agentid2}
            for divisonid, agentid1, agentid2 in cursor.fetchall()
        ]
        if multiple:
            raise MultipleAgentsException(multiple)

        # get the list of collections the agents belong to.
        collections = spmodels.Collection.objects.filter(discipline__division__members__specifyuser_id=userid).values_list('id', flat=True)

        # check permissions for setting user agents in those collections.
        for collectionid in collections:
            check_permission_targets(collectionid, request.specify_user.id, [SetUserAgentsPT.update])

        check_collection_access_against_agents(userid)

    return http.HttpResponse('', status=204)

def check_collection_access_against_agents(userid: int) -> None:
    from specifyweb.context.views import users_collections_for_sp6, users_collections_for_sp7

    # get the list of collections the agents belong to.
    collections = spmodels.Collection.objects.filter(discipline__division__members__specifyuser_id=userid).values_list('id', flat=True)

    # make sure every collection the user is permitted to access has an assigned user.
    sp6_collections = users_collections_for_sp6(connection.cursor(), userid)
    sp7_collections = users_collections_for_sp7(userid)
    missing_for_6 = [
        collectionid
        for collectionid, _ in sp6_collections
        if collectionid not in collections
    ]
    missing_for_7 = [
        collection.id
        for collection in sp7_collections
        if collection.id not in collections
    ]
    if missing_for_6 or missing_for_7:
        all_divisions = spmodels.Division.objects.filter(
            disciplines__collections__id__in=[cid for cid, _ in sp6_collections] + [c.id for c in sp7_collections]
        ).values_list('id', flat=True).distinct()
        raise MissingAgentForAccessibleCollection({
            'missing_for_6': missing_for_6,
            'missing_for_7': missing_for_7,
            'all_accessible_divisions': list(all_divisions),
        })



class Sp6AdminPT(PermissionTarget):
    resource = '/admin/user/sp6/is_admin'
    update = PermissionTargetAction()

@openapi(schema={
    'post': {
        "requestBody": {
            "required": True,
            "description": "Set or clear the admin status for a user.",
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "admin_status": {
                                "type": "string",
                                'enum': ['true', 'false'],
                                "description": "Whether the user should be given admin status.",
                            },
                        },
                        'required': ['admin_status'],
                        'additionalProperties': False
                    }
                }
            }
        },
        "responses": {
            "204": {"description": "Success",},
            "403": {"description": "Logged in user is not an admin."}
        }
    },
})
@login_maybe_required
@require_POST
def set_admin_status(request, userid):
    """Sets <userid> specify user's is-admin status to 'true' or 'false'
    according to the 'admin_status' POST parameter. Must be logged in
    as an admin, otherwise HTTP 403 is returned.
    """
    check_permission_targets(None, request.specify_user.id, [Sp6AdminPT.update])
    user = spmodels.Specifyuser.objects.get(pk=userid)
    if request.POST['admin_status'] == 'true':
        user.set_admin()
        return http.HttpResponse('true', content_type='text/plain')
    else:
        user.clear_admin()
        return http.HttpResponse('false', content_type='text/plain')

class ReplaceRecordPT(PermissionTarget):
    resource = "/record/replace"
    update = PermissionTargetAction()
    delete = PermissionTargetAction()


# Returns QuerySet which selects and locks entries when evaluated
def filter_and_lock_target_objects(model, ids, name):
    query: Q = Q(**{name: ids[0]})
    for old_model_id in ids[1:]:
        query.add(Q(**{name: old_model_id}), Q.OR)
    return model.objects.filter(query).select_for_update()

def add_ordering_to_key(table_name):
    ordering_fields = orderings.get(table_name, ())
    def ordered_keys(object, previous_fields):
        with_order = [-1*getattr(object, field, None) for field in ordering_fields]
        # FEATURE: Allow customizing this
        with_order.extend([getattr(object, field, None) for field in previous_fields])
        return tuple(with_order)

    return ordered_keys

class FailedMergingException(Exception):
    pass

def resolve_record_merge_response(start_function, silent=True):
    try:
        response = start_function()
    except Exception as error:
        # FEATURE: Add traceback here
        if isinstance(error, FailedMergingException):
            logger.info('FailedMergingException')
            logger.info(error.args[0])
            logger.info(traceback.format_exc())
            response = error.args[0]
        elif silent:
            logger.info(traceback.format_exc())
            return http.HttpResponseServerError(content=str(traceback.format_exc()), content_type="application/json")
        else:
            raise
    return response

Progress = Callable[[int, int], None]

# Case specific table that can be executed all once to improve merging performance.
# Only use if it can be assured that no constraints will be raised, requiring recursive merging.
# Maps a tuple of the target record's table and the foreign table to a list of the columns to be updated
MERGING_OPTIMIZATION_FIELDS = {
    'agent': {
        'spauditlog': ['createdbyagent_id', 'modifiedbyagent_id'],
        'taxon': ['createdbyagent_id', 'modifiedbyagent_id'],
        'collectionobject': ['createdbyagent_id', 'modifiedbyagent_id']
    }
}

# TODO: Refactor this to always use query sets.
def clean_fields_pre_delete(obj_instance):
    if (not obj_instance.__class__.__name__.endswith('attachment')
            or not hasattr(obj_instance, 'attachment')) :
        return
    # We delete this object anyways. So, don't care about
    # the value we put in here. If an error, everything is rollbacked.
    obj_instance.attachment.attachmentlocation = None

ordering_tables = {
    table_name.lower(): fields for table_name, fields in orderings.items()
}

def fix_orderings(base_model: Table, new_record_data):
    for field_name, records in list(new_record_data.items()):
        try:
            relationship = base_model.get_relationship(field_name)
        except FieldDoesNotExistError:
            continue
        ordering_fields = ordering_tables.get(relationship.relatedModelName.lower(), None)
        if (ordering_fields is None or
                # Can this ever happen?
                not isinstance(records, list)):
            continue
        order_fields_data = set([tuple([record.get(ordering_field, None)
                              for ordering_field in ordering_fields])
                                for record in records])

        if len(order_fields_data) != len(records):
            resources = []
            for record in records:
                is_new = 'id' not in record
                for ordering_field in ordering_fields:
                    # Directly take the order whatever front-end gave for the old resources.
                    # Assuming that old resources had valid ordering fields. Otherwise, uniqueness error is thrown.
                    # TODO: If causes a problem, try guessing the best ordering fields for old resources
                    record.update({ordering_field: record.get(ordering_field) if not is_new else None})
                # This is done to make sure new resources aren't created before old ones are saved
                # otherwise uniqueness constraints are violated
                if is_new:
                    resources.append(record)
                else:
                    resources.insert(0, record)
            new_record_data[field_name] = resources

def fix_record_data(new_record_data, current_model: Table, target_model_name: str, new_record_id, old_record_ids):
    return_data = {}

    for field_name, value in list(new_record_data.items()):
        model_field = current_model.get_field(field_name)
        return_data[field_name] = value
        if (model_field is None or
                (not model_field.is_relationship)):
            continue

        if (isinstance(value, str)
                and (model_field.relatedModelName.lower()
                     == target_model_name)):

            new_uri = uri_for_model(target_model_name, new_record_id)
            for old_id in old_record_ids:
                old_uri = uri_for_model(target_model_name, old_id)
                value = value.replace(old_uri, new_uri)
                
        elif isinstance(value, list):
            value = [(fix_record_data(dep_data, spmodels.datamodel.get_table(model_field.relatedModelName), target_model_name, new_record_id, old_record_ids))
                       for dep_data in value]
        return_data[field_name] = value

    return return_data
@transaction.atomic
def record_merge_fx(model_name: str, old_model_ids: List[int], new_model_id: int,
                    progress: Optional[Progress]=None,
                    new_record_info: Dict[str, Any]=None) -> http.HttpResponse:
    """Replaces all the foreign keys referencing the old record ID
    with the new record ID, and deletes the old record.
    """
    # Confirm the target model table exists
    model_name = model_name.lower().title()
    target_model = getattr(spmodels, model_name)
    if target_model is None:
        raise FailedMergingException(http.HttpResponseNotFound("model_name: " + model_name + "does not exist."))

    # Check to make sure both the old and new agent IDs exist in the table
    if not target_model.objects.filter(id=new_model_id).select_for_update().exists():
        raise FailedMergingException(http.HttpResponseNotFound(model_name + "ID: " + str(new_model_id) + " does not exist."))
    for old_model_id in old_model_ids:
        if not target_model.objects.filter(id=old_model_id).select_for_update().exists():
            raise FailedMergingException(http.HttpResponseNotFound(model_name + "ID: " + str(old_model_id) + " does not exist."))

    # Get dependent fields and objects of the target object
    target_object = target_model.objects.get(id=new_model_id)
    dependant_relationships = [(rel.relatedModelName, rel.name)
        for rel in target_object.specify_model.relationships
        if api.is_dependent_field(target_object, rel.name)]

    dependant_table_names = set([rel[0] for rel in dependant_relationships])

    # Get all of the columns in all of the tables of specify the are foreign keys referencing model ID
    foreign_key_cols = []
    for table in spmodels.datamodel.tables:
        for relationship in table.relationships:
            if relationship.relatedModelName.lower() == model_name.lower():
                foreign_key_cols.append((table.name, relationship.name))
    progress(0, len(foreign_key_cols)) if progress is not None else None

    # Build query to update all of the records with foreign keys referencing the model ID
    for table_name, column_names in groupby(foreign_key_cols, lambda x: x[0]):
        foreign_table = spmodels.datamodel.get_table(table_name)
        if foreign_table is None:
            continue
        try:
            foreign_model = getattr(spmodels, table_name.lower().title())
        except ValueError:
            continue

        # Handle case of updating a large amount of record ids in a foreign table.
        # Example: handle case of updating a large amount of agent ids in the audit logs.
        # Fix by optimizing the query by consolidating it here
        if model_name.lower() in MERGING_OPTIMIZATION_FIELDS and \
            table_name.lower() in MERGING_OPTIMIZATION_FIELDS[model_name.lower()]:
            for field_name in MERGING_OPTIMIZATION_FIELDS[model_name.lower()][table_name.lower()]:
                query = Q(**{field_name: old_model_ids[0]})
                for old_model_id in old_model_ids[1:]:
                    query.add(Q(**{field_name: old_model_id}), Q.OR)
                foreign_model.objects.filter(query).update(**{field_name: new_model_id})
                progress(1, 0) if progress is not None else None
            continue

        apply_order = add_ordering_to_key(table_name.lower().title())
        # BUG: timestampmodified could be null for one record, and not the other
        new_key_fields = ('timestampcreated', 'timestampmodified', 'id') \
            if foreign_table.get_field('timestampCreated') is not None \
            else ()  # Consider using id here

        key_function = lambda x: apply_order(x, new_key_fields)

        for col in [c[1] for c in column_names]:
            progress(1, 0) if progress is not None else None
            
            # Determine the field name to filter on
            field_name = col.lower()
            field_name_id = f'{field_name}_id'
            if not hasattr(foreign_model, field_name_id):
                continue

            # Filter the objects in the foreign model that references the old target model
            foreign_objects = filter_and_lock_target_objects(foreign_model, old_model_ids, field_name_id)

            # Update and save the foreign model objects with the new_model_id.
            # Locking foreign objects in the beginning because another transaction could update records, and we will 
            # then either overwrite or delete that change if we iterate to it much later.
            for obj in foreign_objects:
                # If it is a dependent field, delete the object instead of updating it.
                # This is done in order to avoid duplicates
                if table_name in dependant_table_names:
                    # Note: need to handle case where deletion throws error because it is referenced my other records
                    try:
                        clean_fields_pre_delete(obj)
                        obj.delete()
                    except ProtectedError as e:
                        # NOTE: Handle ProtectedError in the future.
                        # EXAMPLE: ProtectedError: ("Cannot delete some instances of model 'Address' because they are 
                        # referenced through protected foreign keys:
                        # 'Division.address'.", {<Division: Division object (2)>})
                        raise
                    continue

                # Set new value for the field
                setattr(obj, field_name_id, new_model_id)

                def record_merge_recur(row_to_lock=None):
                    """ Recursively run another merge process to resolve uniqueness constraints.
                        TODO: Add more sanity checks here.

                        An important, and hard to catch case being missed:
                        Between the exception being raised, and record_merge_recur setting a lock, another transaction 
                        could alter the row, and cause the uniqueness constraint to be invalid. In this case, we would 
                        delete a record that we didn't need to.
                    """

                    # Probably could lock more rows than needed.
                    # We immediately rollback if more than 1, so this is fine.
                    foreign_record_lst = filter_and_lock_target_objects(foreign_model, row_to_lock, 'id') \
                        if row_to_lock is not None \
                        else foreign_model.objects.filter(**{field_name_id: new_model_id}).select_for_update()

                    foreign_record_count = foreign_record_lst.count()

                    if foreign_record_count > 1:
                        # NOTE: Maybe try handling multiple possible row that are potentially causes the conflict.
                        # Would have to go through all constraints and check records based on columns in each constraint.
                        # This case probably is no longer needed to be handled since records are fetched by primary
                        # keys now, and uniqueness constraints are handled via business exceptions.

                        raise FailedMergingException(http.HttpResponseNotAllowed(
                            'Error! Multiple records violating uniqueness constraints in ' + table_name))

                    # Determine which of the records will be assigned as old and new with the timestampcreated field
                    old_record = obj
                    new_record = foreign_record_lst.first()
                    old_record, new_record = sorted([old_record, new_record], key=key_function)

                    # Make a recursive call to record_merge to resolve duplication error
                    response = record_merge_fx(table_name, [old_record.pk], new_record.pk, progress)
                    if old_record.pk != obj.pk:
                        update_record(new_record)
                    return response

                def update_record(record: models.Model):
                    try:
                        # TODO: Handle case where this obj has been deleted from recursive merge
                        with transaction.atomic():
                            record.save()
                    except (IntegrityError, BusinessRuleException) as e:
                        # Catch duplicate error and recursively run record merge
                        rows_to_lock = None
                        if isinstance(e, BusinessRuleException) \
                                and 'must have unique' in str(e) \
                                and e.args[1]['table'].lower() == table_name.lower():
                            # Sanity check because rows can be deleted
                            rows_to_lock = e.args[1]['conflicting']
                            return record_merge_recur(rows_to_lock)
                            # As long as business rules are updated, this shouldn't be raised.
                            # Still having it for completeness
                        elif e.args[0] == 1062 and "Duplicate" in str(e):
                            return record_merge_recur()
                        else:
                            raise

                response: http.HttpResponse = update_record(obj)
                if response is not None and response.status_code != 204:
                    return response

    # Dedupe by deleting the record that is being replaced and updating the old model ID to the new one
    for old_model_id in old_model_ids:
        target_model.objects.get(id=old_model_id).delete()

    # Update new record with json info, if given
    has_new_record_info = new_record_info is not None
    if has_new_record_info and 'new_record_data' in new_record_info and \
            new_record_info['new_record_data'] is not None:
        try:
            for table_name, _field_name in dependant_relationships:
                # minor optimization to not fetch unnecessary dependent resources
                if not table_name.lower().endswith('attachment'):
                    continue
                field_name = _field_name.lower()
                # put_resource will drop existing dependent resources.
                # this will trigger deletion from asset server.
                # so, cleaning fields here. It does this for all
                # attachments, which is fine since we just use
                # whatever front-end sends as the final data
                [clean_fields_pre_delete(dependent_object)
                 for dependent_object in getattr(target_object, field_name).all()
                 ]
            new_record_data = new_record_info['new_record_data']
            target_table = spmodels.datamodel.get_table(model_name.lower())
            fix_orderings(target_table, new_record_data)
            obj = api.put_resource(new_record_info['collection'],
                                   new_record_info['specify_user'],
                                   model_name,
                                   new_model_id,
                                   new_record_info['version'],
                                   fix_record_data(new_record_data, target_table, target_table.name.lower(), new_model_id, old_model_ids))
        except IntegrityError as e:
            # NOTE: Handle IntegrityError Duplicate entry in the future.
            # EXAMPLE: IntegrityError: (1062, "Duplicate entry '1-0' for key 'AgentID'")
            raise

    # Return http response
    return http.HttpResponse('', status=204)

@app.task(base=LogErrorsTask, bind=True)
def record_merge_task(self, model_name: str, old_model_ids: List[int], new_model_id: int, merge_id: int,
                      new_record_dict: Dict[str, Any]=None):
    "Run the record merging process as a background task with celery"

    logger.info('logging is working for record merging task')
    logger.info(f'starting task {str(self.request.id)}')

    specify_user_id = new_record_dict['specify_user_id']
    specify_user_agent_id = new_record_dict['specify_user_agent_id']
    specify_user = spmodels.Specifyuser.objects.get(id=specify_user_id)
    specify_user_agent = spmodels.Agent.objects.get(id=specify_user_agent_id)

    new_record_info = {
        'agent_id': new_record_dict['agent_id'],
        'collection': spmodels.Collection.objects.get(id=new_record_dict['collection_id']),
        'specify_user': specify_user_agent,
        'version': new_record_dict['version'],
        'new_record_data': new_record_dict['new_record_data']
    }

    # Track the progress of the record merging
    current = 0
    total = 1
    def progress(cur: int, additional_total: int=0) -> None:
        nonlocal current, total
        current += cur
        total += additional_total
        if current > total:
            current = total
        if not self.request.called_directly:
            self.update_state(state='MERGING', meta={'current': current, 'total': total})

    # Run the record merging function
    logger.info('Starting record merge')

    response = resolve_record_merge_response(
        lambda: record_merge_fx(model_name, old_model_ids, int(new_model_id), progress, new_record_info))

    logger.info('Finishing record merge')

    # Update the finishing state of the record merging process
    merge_record = Spmerging.objects.get(id=merge_id)
    if response.status_code != 204:
        self.update_state(state='FAILED', meta={'current': current, 'total': total})
        merge_record.mergingstatus = 'FAILED'
    else:
        self.update_state(state='SUCCEEDED', meta={'current': total, 'total': total})
        merge_record.mergingstatus = 'SUCCEEDED'
    
    merge_record.response = response.content.decode()
    merge_record.save()

    # Create a message record to indicate the finishing status of the record merge
    logger.info('Creating finishing message')
    if response.status_code == 204:
        logger.info('Merge Succeeded!')
    else:
        logger.info('Merge Failed!')

    Message.objects.create(user=specify_user, content=json.dumps({
        'type': 'record-merge-succeeded' if response.status_code == 204 else 'record-merge-failed',
        'response': response.content.decode(),
        'task_id': self.request.id,
        'table': model_name.title(),
        'new_record_id': new_model_id,
        'old_record_ids': json.dumps(old_model_ids)
    }))

@openapi(schema={
    'post': {
        "requestBody": {
            "required": True,
            "description": "Replace a list of old records with a new record.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "description": "The request body.",
                        "properties": {
                            "model_name": {
                                "type": "string",
                                "description": "The name of the table that is to be merged."
                            },
                            "new_model_id": {
                                "type": "integer",
                                "description": "The new ID value of the model that is replacing the old one."
                            },
                            "old_record_ids": {
                                "type": "array",
                                "items": {
                                    "type": "integer"
                                },
                                "description": "The old record IDs."
                            },
                            "new_record_data": {
                                "type": "object",
                                "description": "The new record data."
                            },
                            "background": {
                                "type": "boolean",
                                "description": "Determine if the merging should be done as a background task.  Default is True."
                            }
                        },
                        'required': ['model_name', 'new_model_id', 'collection_id', 'old_record_ids', 'new_record_data'],
                        'additionalProperties': False
                    }
                }
            }
        },
        "responses": {
            "204": {"description": "Success",},
            "404": {"description": "The ID specified does not exist."},
            "405": {"description": "A database rule was broken."}
        }
    },
})
@login_maybe_required
@require_POST
def record_merge(
    request: http.HttpRequest, 
    model_name: str, 
    new_model_id: int
) -> Union[http.HttpResponse, http.JsonResponse]:
    """Replaces all the foreign keys referencing the old record IDs
    with the new record ID, and deletes the old records.
    """
    record_version = getattr(spmodels, model_name.title()).objects.get(id=new_model_id).version
    get_version = request.GET.get('version', record_version)
    version = get_version if isinstance(get_version, int) else 0

    table_permissions_checker(request.specify_collection, request.specify_user_agent, "read")
    check_permission_targets(request.specify_collection.id, request.specify_user.id, [ReplaceRecordPT.update, ReplaceRecordPT.delete])

    data = json.loads(request.body)
    old_model_ids = data['old_record_ids']
    new_record_data = data['new_record_data'] if 'new_record_data' in data else None

    if old_model_ids is None or len(old_model_ids) < 1:
        return http.HttpResponseBadRequest('There were no old record IDs given to be replaced by the new ID.')
    
    background = True
    if 'background' in data:
        background = data['background']

    if background:
        # Check if another merge is still in progress
        cur_merges = Spmerging.objects.filter(mergingstatus='MERGING')
        for cur_merge in cur_merges:
            cur_task_id = cur_merge.taskid
            cur_result = record_merge_task.AsyncResult(cur_task_id)
            if cur_result is not None:
                cur_merge.mergingstatus = 'FAILED'
                cur_merge.save()
            elif cur_result.state == 'MERGING':
                return http.HttpResponseNotAllowed(
                    'Another merge process is still running on the system, please try again later.')
            else:
                cur_merge.mergingstatus = cur_result.state
                cur_merge.save()

        # Create task id and a Spmerging record
        task_id = str(uuid4())
        merge = Spmerging.objects.create(
            name = "Merge_" + model_name + "_" + new_model_id,
            taskid = task_id,
            mergingstatus = "MERGING",
            table = model_name.title(),
            newrecordid = new_model_id,
            newrecordata = json.dumps(new_record_data),
            oldrecordids = json.dumps(old_model_ids),
            collection = request.specify_collection,
            specifyuser = request.specify_user,
            createdbyagent = request.specify_user_agent,
            modifiedbyagent = request.specify_user_agent,
        )
        merge.save()

        # Create a notification record of the merging process pending
        Message.objects.create(user=request.specify_user, content=json.dumps({
            'type': 'record-merge-starting',
            'name': "Merge_" + model_name + "_" + new_model_id,
            'task_id': task_id,
            'table': model_name.title(),
            'new_record_id': new_model_id,
            'old_record_ids': old_model_ids,
            'new_record_info': new_record_data,
            'collection_id': request.specify_collection.id
        }))

        new_record_info = {
            'agent_id': int(new_model_id),
            'collection_id': request.specify_collection.id,
            'specify_user_id': request.specify_user.id,
            'specify_user_agent_id': request.specify_user_agent.id,
            'version': version,
            'new_record_data': new_record_data
        }
        
        try:
            json.dumps(new_record_info)
        except TypeError as e:
            return http.HttpResponseNotAllowed('Error while serializing new_record_info')

        # Run the merging process in the background with celery
        async_result = record_merge_task.apply_async(
            [model_name, old_model_ids, int(new_model_id), merge.id, new_record_info],
            task_id=task_id)

        return http.JsonResponse(async_result.id, safe=False)
    else:
        new_record_info = {
            'agent_id': int(new_model_id),
            'collection': request.specify_collection,
            'specify_user': request.specify_user_agent,
            'version': version,
            'new_record_data': new_record_data
        }

        response = resolve_record_merge_response(
            lambda: record_merge_fx(model_name, old_model_ids, int(new_model_id), None, new_record_info),
            # If not doing merge in background, raise all unexpected errors
            silent=False
        )
    return response


CELERY_MERGE_STATUS_MAP = {
    'PENDING': 'PENDING',
    'STARTED': 'MERGING',
    'SUCCESS': 'SUCCEEDED',
    'FAILURE': 'FAILED',
    'RETRY': 'MERGING',
    'REVOKED': 'FAILED',
    'REJECTED': 'FAILED'
}

@openapi(schema={
    'get': {
        "responses": {
            "200": {
                "description": "Data fetched successfully",
                "content": {
                    "text/plain": {
                        "schema": {
                            "oneOf": [
                                {
                                    "type": "string",
                                    "example": "null",
                                    "description": "Nothing to report"
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "taskprogress": {
                                            "type": "object",
                                            "properties": {
                                                "current": {
                                                    "type": "number",
                                                    "example": 11,
                                                },
                                                "total": {
                                                    "type": "number",
                                                    "example": 22,
                                                }
                                            }
                                        },
                                        "taskstatus": {
                                            "type": "string",
                                            "enum": [
                                                "MERGING",
                                                "SUCCEEDED",
                                                "FAILED",
                                                "ABORTED"
                                            ]
                                        },
                                        "taskid": {
                                            "type": "string",
                                            "maxLength": 36,
                                            "example": "7d34dbb2-6e57-4c4b-9546-1fe7bec1acca"
                                        },
                                    },
                                    "description": "Status of the record merge process",
                                }
                            ]
                        }
                    }
                }
            },
        }
    },
})
@require_GET
def merging_status(request, merge_id: int) -> http.HttpResponse:
    """Returns the merging status for the record merging celery tasks"""
    
    # Try to get the merge object directly
    try:
        merge = Spmerging.objects.get(taskid=merge_id)
    except Spmerging.DoesNotExist:
        return http.HttpResponseNotFound(f'The merge task id is not found: {merge_id}')

    task_status = merge.mergingstatus
    task_progress = None

    try:
        result = record_merge_task.AsyncResult(merge.taskid)
        task_progress = result.info if isinstance(result.info, dict) else repr(result.info)
        
        # Update task status if necessary
        if result.state not in ['PENDING', 'STARTED', 'SUCCESS', 'RETRY']:
            task_status = CELERY_MERGE_STATUS_MAP.get(result.state, task_status)
    except Exception:
        pass

    status = {
        'taskstatus': merge.mergingstatus,
        'response': merge.response,
        'taskprogress': result.info if isinstance(result.info, dict) else repr(result.info),
        'taskid': merge.taskid
    }

    return http.JsonResponse(status)

@openapi(schema={
    'post': {
        'responses': {
            '200': {
                'description': 'The task has been successfully aborted or it is not running and cannot be aborted',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'message': {
                                    'type': 'string',
                                    'description': 'Response message about the status of the task'
                                },
                            },
                        },
                    },
                },
            },
            '404': {
                'description': 'The merge task id is not found',
            },
            '400': {
                'description': 'Invalid input, object invalid',
            },
        },
    },
})
@require_POST
def abort_merge_task(request, merge_id: int) -> http.HttpResponse:
    "Aborts the merge task currently running and matching the given merge/task ID"

    merge = Spmerging.objects.get(taskid=merge_id)
    if merge is None:
        return http.HttpResponseNotFound(f'The merge task id is not found: {merge_id}')

    if merge.taskid is None:
        return http.JsonResponse(None, safe=False)

    task = record_merge_task.AsyncResult(merge.taskid)
    
    if task.state == 'PENDING' or task.state == 'MERGING':
        # Revoking and terminating the task
        app.control.revoke(merge.taskid, terminate=True)

        # Updating the merging status
        merge.mergingstatus = 'ABORTED'
        merge.save()

        # Send notification the the megre task has been aborted
        Message.objects.create(user=request.specify_user, content=json.dumps({
            'type': 'record-merge-aborted',
            'name': "Merge_" + merge.table.title() + "_" + str(merge.newrecordid),
            'task_id': merge_id,
            'table': merge.table,
            'new_record_id': merge.newrecordid,
            'collection_id': request.specify_collection.id,
        }))

        return http.HttpResponse(f'Task {merge.taskid} has been aborted.')

    else:
        return http.HttpResponse(f'Task {merge.taskid} is not running and cannot be aborted.')
