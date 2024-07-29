from functools import wraps
from typing import Literal, Tuple
from django.db import transaction
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_POST
from sqlalchemy import sql
from sqlalchemy.orm import aliased

from specifyweb.middleware.general import require_GET
from specifyweb.businessrules.exceptions import BusinessRuleException
from specifyweb.permissions.permissions import PermissionTarget, \
    PermissionTargetAction, check_permission_targets, has_table_permission
from specifyweb.specify.tree_ranks import tree_rank_count
from specifyweb.specify import models
from specifyweb.stored_queries import models as sqlmodels
from . import tree_extras
from .api import get_object_or_404, obj_to_data, toJson
from .auditcodes import TREE_MOVE
from .tree_stats import get_tree_stats
from .views import login_maybe_required, openapi

import logging
logger = logging.getLogger(__name__)

TREE_TABLE = Literal['Taxon', 'Storage',
                     'Geography', 'Geologictimeperiod', 'Lithostrat']

COMMON_TREES: Tuple[TREE_TABLE, ...] = ['Taxon', 'Storage',
                                        'Geography']

ALL_TRESS: Tuple[TREE_TABLE, ...] = [
    *COMMON_TREES, 'Geologictimeperiod', 'Lithostrat']


def tree_mutation(mutation):
    @login_maybe_required
    @require_POST
    @transaction.atomic
    @wraps(mutation)
    def wrapper(*args, **kwargs):
        try:
            mutation(*args, **kwargs)
            result = {'success': True}
        except BusinessRuleException as e:
            result = {'success': False, 'error': str(e)}
        return HttpResponse(toJson(result), content_type="application/json")

    return wrapper


@openapi(schema={
    "get": {
        "parameters": [
            {
                "name": "includeauthor",
                "in": "query",
                "required": False,
                "schema": {
                    "type": "number"
                },
                "description": "If parameter is present, include the author of the requested node in the response \
                    if the tree is taxon and node's rankid >= paramter value."
            }
        ],
        "responses": {
            "200": {
                "description": "Returns a list of nodes with parent <parentid> restricted to the tree defined by <treedef>. \
                Nodes are sorted by <sortfield>",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "array",
                                "prefixItems": [
                                    {

                                        "type": "integer",
                                        "description": "The id of the child node"

                                    },
                                    {
                                        "type": "string",
                                        "description": "The name of the child node"
                                    },
                                    {
                                        "type": "string",
                                        "description": "The fullName of the child node"
                                    },
                                    {

                                        "type": "integer",
                                        "description": "The nodenumber of the child node"
                                    },
                                    {
                                        "type": "integer",
                                        "description": "The highestChildNodeNumber of the child node"
                                    },
                                    {
                                        "type": "integer",
                                        "description": "The rankId of the child node"

                                    },
                                    {
                                        "type": "number",
                                        "description": "The acceptedId of the child node. Returns null if the node has no acceptedId"
                                    },
                                    {
                                        "type": "string",
                                        "description": "The fullName of the child node's accepted node. Returns null if the node has no acceptedId"
                                    },
                                    {
                                        "type": "string",
                                        "description": "The author of the child node. \
                                        Returns null if <tree> is not taxon or the rankId of the node is less than <includeAuthor> paramter"
                                    },
                                    {

                                        "type": "integer",
                                        "description": "The number of children the child node has"

                                    }
                                ],
                            }
                        }
                    }
                }
            }
        }
    }
})
@login_maybe_required
@require_GET
def tree_view(request, treedef, tree: TREE_TABLE, parentid, sortfield):
    """Returns a list of <tree> nodes with parent <parentid> restricted to
    the tree defined by treedefid = <treedef>. The nodes are sorted
    according to <sortfield>.
    """
    tree_table = models.datamodel.get_table(tree)
    parentid = None if parentid == 'null' else int(parentid)

    node = getattr(sqlmodels, tree_table.name)
    child = aliased(node)
    accepted = aliased(node)
    id_col = getattr(node, node._id)
    child_id = getattr(child, node._id)
    treedef_col = getattr(node, tree_table.name + "TreeDefID")
    orderby = tree_table.name.lower() + '.' + sortfield

    """
        Also include the author of the node in the response if requested and the tree is the taxon tree.
        There is a preference which can be enabled from within Specify which adds the author next to the 
        fullname on the front end. 
        See https://github.com/specify/specify7/pull/2818 for more context and a breakdown regarding 
        implementation/design decisions
    """
    includeAuthor = request.GET.get(
        'includeauthor') if 'includeauthor' in request.GET else False

    with sqlmodels.session_context() as session:
        query = session.query(id_col,
                              node.name,
                              node.fullName,
                              node.nodeNumber,
                              node.highestChildNodeNumber,
                              node.rankId,
                              node.AcceptedID,
                              accepted.fullName,
                              node.author if (
                                  includeAuthor and tree == 'taxon') else "NULL",
                              sql.functions.count(child_id)) \
            .outerjoin(child, child.ParentID == id_col) \
            .outerjoin(accepted, node.AcceptedID == getattr(accepted, node._id)) \
            .group_by(id_col) \
            .filter(treedef_col == int(treedef)) \
            .filter(node.ParentID == parentid) \
            .order_by(orderby)
        results = list(query)
    return HttpResponse(toJson(results), content_type='application/json')


@login_maybe_required
@require_GET
def tree_stats(request, treedef, tree, parentid):
    "Returns tree stats (collection object count) for tree nodes parented by <parentid>."

    using_cte = (tree in ['geography', 'taxon', 'storage'])
    results = get_tree_stats(
        treedef, tree, parentid, request.specify_collection, sqlmodels.session_context, using_cte)

    return HttpResponse(toJson(results), content_type='application/json')


@login_maybe_required
@require_GET
def path(request, tree: TREE_TABLE, id: int):
    "Returns all nodes up to the root of <tree> starting from node <id>."
    id = int(id)
    tree_node = get_object_or_404(tree, id=id)

    data = {node.definitionitem.name: obj_to_data(node)
            for node in get_tree_path(tree_node)}

    data['resource_uri'] = '/api/specify_tree/%s/%d/path/' % (tree, id)

    return HttpResponse(toJson(data), content_type='application/json')


def get_tree_path(tree_node):
    while tree_node is not None:
        yield tree_node
        tree_node = tree_node.parent


@login_maybe_required
@require_GET
def predict_fullname(request, tree: TREE_TABLE, parentid: int):
    """Returns the predicted fullname for a <tree> node based on the name
    field of the node and its <parentid>. Requires GET parameters
    'treedefitemid' and 'name', to indicate the rank (treedefitem) and
    name of the node, respectively.
    """
    parent = get_object_or_404(tree, id=parentid)
    depth = parent.definition.treedefitems.count()
    reverse = parent.definition.fullnamedirection == -1
    defitemid = int(request.GET['treedefitemid'])
    name = request.GET['name']
    fullname = tree_extras.predict_fullname(
        parent._meta.db_table, depth, parent.id, defitemid, name, reverse
    )
    return HttpResponse(fullname, content_type='text/plain')


@tree_mutation
def merge(request, tree: TREE_TABLE, id: int):
    """Merges <tree> node <id> into the node with id indicated by the
    'target' POST parameter."""
    check_permission_targets(request.specify_collection.id,
                             request.specify_user.id, [perm_target(tree).merge])
    node = get_object_or_404(tree, id=id)
    target = get_object_or_404(tree, id=request.POST['target'])
    tree_extras.merge(node, target, request.specify_user_agent)


@tree_mutation
def move(request, tree: TREE_TABLE, id: int):
    """Reparents the <tree> node <id> to be a child of the node
    indicated by the 'target' POST parameter.
    """
    check_permission_targets(request.specify_collection.id,
                             request.specify_user.id, [perm_target(tree).move])
    node = get_object_or_404(tree, id=id)
    target = get_object_or_404(tree, id=request.POST['target'])
    old_parent = node.parent
    old_parentid = old_parent.id
    old_fullname = node.fullname
    node.parent = target
    old_stamp = node.timestampmodified
    node.save()
    node = get_object_or_404(tree, id=id)
    if old_stamp is None or (node.timestampmodified > old_stamp):
        tree_extras.mutation_log(TREE_MOVE, node, request.specify_user_agent,
                                 node.parent,
                                 [{'field_name': 'parentid',
                                   'old_value': old_parentid,
                                   'new_value': target.id},
                                  {'field_name': 'fullname',
                                   'old_value': old_fullname,
                                   'new_value': node.fullname}])


@openapi(schema={
    "post": {
        "parameters": [{
            "name": "tree",
            "in": "path",
            "required": True,
            "schema": {
                "enum": ['Storage']
            }
        },
            {
            "name": "id",
            "in": "path",
            "description": "The id of the node from which to bulk move from.",
            "required": True,
            "schema": {
                "type": "integer",
                "minimum": 0
            }
        }],
        "requestBody": {
            "required": True,
            "content": {
                "application/x-www-form-urlencoded": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "target": {
                                "type": "integer",
                                "description": "The ID of the storage tree node to which the preparations should be moved."
                            },
                        },
                        'required': ['target'],
                        'additionalProperties': False
                    }
                }
            }
        },
        "responses": {
            "200": {
                "description": "Success message indicating the bulk move operation was successful."
            }
        }
    }
})
@tree_mutation
def bulk_move(request, tree: TREE_TABLE, id: int):
    """Bulk move the preparations under the <tree> node <id> to have
    as new location storage the node indicated by the 'target'
    POST parameter.
    """
    check_permission_targets(request.specify_collection.id,
                             request.specify_user.id, [perm_target(tree).bulk_move])
    node = get_object_or_404(tree, id=id)
    target = get_object_or_404(tree, id=request.POST['target'])
    tree_extras.bulk_move(node, target, request.specify_user_agent)


@tree_mutation
def synonymize(request, tree: TREE_TABLE, id: int):
    """Synonymizes the <tree> node <id> to be a synonym of the node
    indicated by the 'target' POST parameter.
    """
    check_permission_targets(request.specify_collection.id,
                             request.specify_user.id,
                             [perm_target(tree).synonymize])
    node = get_object_or_404(tree, id=id)
    target = get_object_or_404(tree, id=request.POST['target'])
    tree_extras.synonymize(node, target, request.specify_user_agent)


@tree_mutation
def desynonymize(request, tree: TREE_TABLE, id: int):
    "Causes the <tree> node <id> to no longer be a synonym of another node."
    check_permission_targets(request.specify_collection.id,
                             request.specify_user.id,
                             [perm_target(tree).desynonymize])
    node = get_object_or_404(tree, id=id)
    tree_extras.desynonymize(node, request.specify_user_agent)


@tree_mutation
def repair_tree(request, tree: TREE_TABLE):
    "Repairs the indicated <tree>."
    check_permission_targets(request.specify_collection.id,
                             request.specify_user.id,
                             [perm_target(tree).repair])
    tree_model = models.datamodel.get_table(tree)
    table = tree_model.name.lower()
    tree_extras.renumber_tree(table)
    tree_extras.validate_tree_numbering(table)


@login_maybe_required
@require_GET
def tree_rank_item_count(request, tree, rankid):
    """Returns the number of items in the tree rank with id <rank_id>."""
    tree_rank_model_name = tree if tree.endswith(
        'treedefitem') else tree + 'treedefitem'
    rank = get_object_or_404(tree_rank_model_name, id=rankid)
    count = tree_rank_count(tree, rank.id)
    return HttpResponse(toJson(count), content_type='application/json')


@openapi(schema={
    "get": {
        "responses": {
            "200": {
                "description": 'Tree information fetched successfully',
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            'properties': {
                                tree: {"$ref": "#/components/schemas/tree_info"} for tree in ALL_TRESS
                            }
                        }
                    }
                }
            }
        }
    }
}, components={
    "schemas": {
        'tree_info': {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "definition": {
                        "type": "object",
                        "description": "A serialized TreeDef",
                    },
                    "ranks": {
                        "type": "array",
                        "description": "An array of the TreeDef's TreeDefItems, sorted by ascending rankid",
                        "items": {
                            "type": "object",
                            "description": "A serialized TreeDefItem"
                        }
                    }
                }
            }
        }
    }
})
@login_maybe_required
@require_GET
def all_tree_information(request):
    def has_tree_read_permission(tree: TREE_TABLE) -> bool:
        return has_table_permission(
            request.specify_collection.id, request.specify_user.id, tree, 'read')

    is_paleo_discipline = request.specify_collection.discipline.is_paleo()

    accessible_trees = tuple(filter(
        has_tree_read_permission, ALL_TRESS if is_paleo_discipline else COMMON_TREES))

    result = {}

    for tree in accessible_trees:
        result[tree] = []

        treedef_model = getattr(models, f'{tree.lower().capitalize()}treedef')
        tree_defs = treedef_model.objects.all()
        for definition in tree_defs:
            ranks = definition.treedefitems.order_by('rankid')
            if tree == 'Taxon': # Filter Taxon tree definitions by discipline
                if (
                    definition.discipline.id != request.specify_collection.discipline.id
                    and not models.CollectionObjectType.objects.filter(
                        taxontreedef=definition,
                        collection__discipline=request.specify_collection.discipline,
                    ).exists()
                ):
                    continue
            
            result[tree].append({
                'definition': obj_to_data(definition),
                'ranks': [obj_to_data(rank) for rank in ranks]
            })

    return HttpResponse(toJson(result), content_type='application/json')


class TaxonMutationPT(PermissionTarget):
    resource = "/tree/edit/taxon"
    merge = PermissionTargetAction()
    move = PermissionTargetAction()
    synonymize = PermissionTargetAction()
    desynonymize = PermissionTargetAction()
    repair = PermissionTargetAction()


class GeographyMutationPT(PermissionTarget):
    resource = "/tree/edit/geography"
    merge = PermissionTargetAction()
    move = PermissionTargetAction()
    synonymize = PermissionTargetAction()
    desynonymize = PermissionTargetAction()
    repair = PermissionTargetAction()


class StorageMutationPT(PermissionTarget):
    resource = "/tree/edit/storage"
    merge = PermissionTargetAction()
    move = PermissionTargetAction()
    bulk_move = PermissionTargetAction()
    synonymize = PermissionTargetAction()
    desynonymize = PermissionTargetAction()
    repair = PermissionTargetAction()


class GeologictimeperiodMutationPT(PermissionTarget):
    resource = "/tree/edit/geologictimeperiod"
    merge = PermissionTargetAction()
    move = PermissionTargetAction()
    synonymize = PermissionTargetAction()
    desynonymize = PermissionTargetAction()
    repair = PermissionTargetAction()


class LithostratMutationPT(PermissionTarget):
    resource = "/tree/edit/lithostrat"
    merge = PermissionTargetAction()
    move = PermissionTargetAction()
    synonymize = PermissionTargetAction()
    desynonymize = PermissionTargetAction()
    repair = PermissionTargetAction()


def perm_target(tree):
    return {
        'taxon': TaxonMutationPT,
        'geography': GeographyMutationPT,
        'storage': StorageMutationPT,
        'geologictimeperiod': GeologictimeperiodMutationPT,
        'lithostrat': LithostratMutationPT,
    }[tree]
