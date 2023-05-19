from django import http

from specifyweb.permissions.permissions import check_table_permissions
from specifyweb.specify.views import openapi
from django.http import HttpResponse

from ..specify.models import Preparation, Determination, Discipline, Locality
from specifyweb.specify.views import login_maybe_required
import logging

logger = logging.getLogger(__name__)
from django.db import connection

@login_maybe_required
@openapi(schema={
    'get': {
        'responses': {
            '200': {
                'description': 'Returns Global Collection Preparation Stats for Specify',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'additionalProperties': True,
                        }
                    }
                }
            }
        }
    }}, )
def collection_preparations(request) -> HttpResponse:
    check_table_permissions(request.specify_collection, request.specify_user, Preparation, "read")
    cursor = connection.cursor()
    # PREP_BY_TYPE_LOTS
    cursor.execute(
        """
        SELECT pt.Name, count(PreparationID), if(sum(countAmt) is null, 0, sum(countAmt))
        FROM preparation p
                 INNER JOIN preptype pt ON pt.PrepTypeID = p.PrepTypeID
        WHERE CollectionMemberID = %s
        group by pt.Name
        """,
        [request.specify_collection.id]
    )
    prepbytypelots_result = cursor.fetchall()
    preptypelotstotal_dict = {}
    for (name, lots, total) in list(prepbytypelots_result):
        preptypelotstotal_dict[name] = {
            'lots': int(lots),
            'total': int(total)
        }
    return http.JsonResponse(preptypelotstotal_dict)


@login_maybe_required
@openapi(schema={
    'get': {
        'responses': {
            '200': {
                'description': 'Returns Global Collection Locality/Geography Stats for Specify',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'countries': {
                                    'type': 'integer'
                                }
                            }
                        }
                    }
                }
            }
        }
    }}, )
def collection_locality_geography(request, stat) -> HttpResponse:
    geography_dict = {}
    if stat == 'percentGeoReferenced':
        geography_dict[stat] = get_percent_georeferenced(request)
    return http.JsonResponse(geography_dict)

@login_maybe_required
@openapi(schema={
    'get': {
        'responses': {
            '200': {
                'description': 'Returns Global Collection Type Specimen Stats for Specify',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'additionalProperties': True,
                        }
                    }
                }
            }
        }
    }}, )
def collection_type_specimens(request) -> HttpResponse:
    check_table_permissions(request.specify_collection, request.specify_user,
                            Determination, "read")
    cursor = connection.cursor()
    # TYPE_SPEC_CNT
    cursor.execute(
        """
        SELECT TypeStatusName, count(DeterminationID) AS DeterminationCount
        FROM determination
        WHERE CollectionMemberID = %s
          AND TypeStatusName is not null
          AND IsCurrent
        group by TypeStatusName
        """,
        [request.specify_collection.id]
    )
    type_specific_count_result = cursor.fetchall()
    type_spec_dict = {}
    for (name, value) in list(type_specific_count_result):
        type_spec_dict[name] = int(value)
    return http.JsonResponse(type_spec_dict)

@openapi(schema={
    'get': {
        'responses': {
            '200': {
                'description': 'Returns Global Collection Taxa Represented for Specify',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'additionalProperties': True,
                        }
                    }
                }
            }
        }
    }}, )
def collection_taxa_represented(request) -> HttpResponse:
    cursor = connection.cursor()
    cursor.execute(
        """select rankid, count((taxonid)) from taxon 
	where exists(select 1 from collectionobject join determination AS determination_1 ON 
	((collectionobject.`CollectionID` = 4 and 
		collectionobject.`CollectionObjectID` = determination_1.`CollectionObjectID`) )
		WHERE determination_1.`IsCurrent` = true 
        and determination_1.PreferredTaxonID = taxon.taxonid) group by rankid;
        """
    )
    taxa_represented_count_result = cursor.fetchall()
    taxa_represented_dict = {}
    for (name, value) in list(taxa_represented_count_result):
        taxa_represented_dict[name] = int(value)
    return http.JsonResponse(taxa_represented_dict)

def collection_user():
    return http.Http404

def get_percent_georeferenced(request):
    check_table_permissions(request.specify_collection, request.specify_user,
                            Discipline, "read")
    check_table_permissions(request.specify_collection, request.specify_user,
                            Locality, "read")
    cursor = connection.cursor()
    cursor.execute("""
       SELECT CASE WHEN (SELECT count(*) FROM locality INNER JOIN discipline ON locality.DisciplineID = discipline.DisciplineID WHERE discipline.DisciplineID = %s) = 0 THEN 0 ELSE ((count(localityid) * 1.0) / ((SELECT count(*) FROM locality) * 1.0)) * 100.0 END AS PercentGeoReferencedLocalities FROM locality WHERE not latitude1 is null""",
                   [request.specify_collection.discipline.id])
    percent_georeferenced = cursor.fetchone()[0]
    return percent_georeferenced