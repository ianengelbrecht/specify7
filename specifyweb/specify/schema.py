from typing import Dict, List, Tuple, Union

from django.views.decorators.http import require_GET
from django import http

from django.conf import settings
from .views import login_maybe_required
from .datamodel import (
    datamodel,
    Table,
    Field,
    Relationship,
    TableDoesNotExistError,
)


def base_schema() -> Dict:
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Specify 7 API",
            "version": settings.VERSION,
            "description": "Description of all Specify 7 API endpoints",
            "license": {
                "name": "GPL-2.0 Licence",
                "url": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html",
            },
        },
        "externalDocs": {
            "description": "How to use specifyweb API as a generic webservice",
            "url": "https://github.com/specify/specify7/wiki/Api-Demo",
        },
        "servers": [
            {
                "url": "/",
                "description": "Current Specify 7 Instance",
            },
            {
                "url": "https://sp7demofish.specifycloud.org/",
                "description": "Specify 7 Public Demo Instance",
            },
            {
                "url": "{url}",
                "variables": {
                    "url": {
                        "default": "/",
                    },
                },
                "description": "Custom Specify 7 Server",
            },
        ],
    }


record_version_description = (
    "A version to work with (can be specified in "
    + "Query string, Header or request object's 'version' key)"
)


@login_maybe_required
@require_GET
def openapi(request) -> http.HttpResponse:
    """Returns a OpenAPI spec for the Specify API at "/api/specify/...".
    This is a work in progress.
    """
    spec = {
        **base_schema(),
        "paths": {
            endpoint_url: endpoint_description
            for table in datamodel.tables
            for endpoint_url, endpoint_description in table_to_endpoint(
                table
            )
        },
        "components": {
            "parameters": {
                "limit": {
                    "name": "limit",
                    "in": "query",
                    "description": "Return at most 'limit' items",
                    "required": False,
                    "schema": {
                        "type": "number",
                        "minimum": 1,
                        "default": 20,
                    },
                },
                "offset": {
                    "name": "offset",
                    "in": "query",
                    "description": "Offset the returned records by n records",
                    "required": False,
                    "schema": {
                        "type": "number",
                        "minimum": 1,
                        "default": 0,
                    },
                },
                "domainfilter": {
                    "name": "domainfilter",
                    "in": "query",
                    "description": "Use the logged_in_collection to limit request to relevant items",
                    "required": False,
                    "schema": {
                        "type": "boolean",
                        "default": False,
                    },
                },
                "orderby": {
                    "name": "orderby",
                    "in": "query",
                    "description": "The name of the field to order by",
                    "required": False,
                    "schema": {
                        "type": "string",
                    },
                },
                "collection_recordsetid": {
                    "name": "recordsetid",
                    "in": "query",
                    "description": "Created resources would be added to a recordset with this ID",
                    "required": False,
                    "schema": {
                        "type": "number",
                        "minimum": 0,
                    },
                },
                "version_in_query": {
                    "name": "version",
                    "in": "query",
                    "description": record_version_description,
                    "required": False,
                    "schema": {"type": "number", "minimum": 0},
                },
                "version_in_header": {
                    "name": "HTTP_IF_MATCH",
                    "in": "header",
                    "description": record_version_description,
                    "required": False,
                    "schema": {
                        "type": "number",
                        "minimum": 0,
                    },
                },
                "record_recordsetid": {
                    "name": "recordsetid",
                    "in": "query",
                    "description": "If provided, response would also contain a 'recordset_info' key.",
                    "required": False,
                    "schema": {
                        "type": "number",
                        "minimum": 0,
                    },
                },
            },
            "schemas": {
                **{
                    table.django_name: table_to_schema(table)
                    for table in datamodel.tables
                },
                "_collection_get": {
                    "type": "object",
                    "properties": {
                        "meta": {
                            "type": "object",
                            "properties": {
                                "limit": {
                                    "type": "number",
                                },
                                "offset": {
                                    "type": "number",
                                },
                                "total_count": {
                                    "type": "number",
                                    "description": "Total Number of records from this table. The count depends on the value of 'domainfilter' query parameter",
                                },
                            },
                        }
                    },
                },
                "_resource_get": {
                    "type": "object",
                    "properties": {
                        "recordset_info": {
                            "oneOf": [
                                {
                                    "type": "string",
                                    "description": "null",
                                },
                                {
                                    "type": "object",
                                    "properties": {
                                        "recordsetid": {
                                            "type": "number",
                                            "minimum": 0,
                                        },
                                        "total_count": {
                                            "type": "number",
                                            "minimum": 0,
                                        },
                                        "index": {
                                            "type": "number",
                                            "minimum": 0,
                                        },
                                        "previous": {
                                            "oneOf": [
                                                {
                                                    "type": "string",
                                                    "description": "null",
                                                },
                                                {
                                                    "type": "string",
                                                    "description": "URL for fetching information about the previous record",
                                                    "example": "/api/specify/collectionobject/249/",
                                                    "minimum": 0,
                                                },
                                            ]
                                        },
                                        "next": {
                                            "oneOf": [
                                                {
                                                    "type": "string",
                                                    "description": "null",
                                                },
                                                {
                                                    "type": "string",
                                                    "description": "URL for fetching information about the next record",
                                                    "example": "/api/specify/collectionobject/249/",
                                                    "minimum": 0,
                                                },
                                            ]
                                        },
                                    },
                                },
                            ],
                        }
                    },
                },
            },
        },
    }
    return http.JsonResponse(spec)


@login_maybe_required
@require_GET
def view(request, model: str) -> http.HttpResponse:
    """Returns a JSONSchema for the JSON representation of resources
    of the given <model> type.
    """
    try:
        table = datamodel.get_table_strict(model)
    except TableDoesNotExistError:
        return http.HttpResponseNotFound()

    return http.JsonResponse(table_to_schema(table))


def table_to_endpoint(table: Table) -> List[Tuple[str, Dict]]:
    return [
        (
            "/api/specify/" + table.django_name,
            {
                "get": {
                    "tags": [table.django_name],
                    "summary": "Query multiple records from the "
                    + table.django_name
                    + " table",
                    "description": "Query multiple records from the "
                    + table.django_name
                    + " table",
                    "parameters": [
                        {"$ref": "#/components/parameters/limit"},
                        {"$ref": "#/components/parameters/offset"},
                        {
                            "$ref": "#/components/parameters/domainfilter"
                        },
                        {"$ref": "#/components/parameters/orderby"},
                    ],
                    "responses": {
                        "200": {
                            "description": "Data fetched successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/_collection_get",
                                            },
                                            {
                                                "type": "object",
                                                "properties": {
                                                    "objects": {
                                                        "type": "array",
                                                        "items": {
                                                            "$ref": "#/components/schemas/"
                                                            + table.django_name
                                                        },
                                                    },
                                                },
                                            },
                                        ]
                                    },
                                },
                            },
                        },
                    },
                },
                "post": {
                    "tags": [table.django_name],
                    "summary": "Upload a single record to the "
                    + table.django_name
                    + " table",
                    "description": "Upload a single record to the "
                    + table.django_name
                    + " table",
                    "parameters": [
                        {
                            "$ref": "#/components/parameters/collection_recordsetid"
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "description": "A JSON representation of an object",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/"
                                    + table.django_name
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "A newly created object",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/"
                                        + table.django_name
                                    },
                                },
                            },
                        }
                    },
                },
            },
        ),
        (
            "/api/specify/" + table.django_name + "/{id}",
            {
                "parameters": [
                    {
                        "$ref": "#/components/parameters/version_in_query"
                    },
                    {
                        "$ref": "#/components/parameters/version_in_header"
                    },
                ],
                "get": {
                    "tags": [table.django_name],
                    "summary": "Query and manipulate records from the "
                    + table.django_name
                    + " table",
                    "description": "TODO: description",
                    "parameters": [
                        {
                            "$ref": "#/components/parameters/record_recordsetid"
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Data fetched successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/_resource_get",
                                            },
                                            {
                                                "$ref": "#/components/schemas/"
                                                + table.django_name
                                            },
                                        ]
                                    }
                                }
                            },
                        }
                    },
                },
                "put": {
                    "tags": [table.django_name],
                    "summary": "Update a single record from the "
                    + table.django_name
                    + " table",
                    "description": "Update a single record from the "
                    + table.django_name
                    + " table",
                    "requestBody": {
                        "required": True,
                        "description": "A JSON representation of an object",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "allOf": [
                                        {
                                            "anyOf": [
                                                {
                                                    "type": "object",
                                                    "properties": {
                                                        "version": {
                                                            "description": record_version_description,
                                                            "type": "number",
                                                            "minimum": 0,
                                                        }
                                                    },
                                                }
                                            ],
                                        },
                                        {
                                            "$ref": "#/components/schemas/"
                                            + table.django_name
                                        },
                                    ],
                                }
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "A modified object",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/"
                                        + table.django_name
                                    },
                                },
                            },
                        }
                    },
                },
                "delete": {
                    "tags": [table.django_name],
                    "summary": "Delete a record from the "
                    + table.django_name
                    + " table",
                    "description": "Delete a record from the "
                    + table.django_name
                    + " table",
                    "response": {
                        "204": {
                            "description": "Empty response",
                            "content": {
                                "text/plain": {
                                    "schema": {
                                        "type": "string",
                                        "maxLength": 0,
                                    }
                                }
                            },
                        }
                    },
                },
            },
        ),
    ]


def table_to_schema(table: Table) -> Dict:
    return {
        "title": table.django_name,
        "type": "object",
        "properties": {
            f.name.lower(): field_to_schema(f) for f in table.all_fields
        },
        "additionalProperties": False,
        "required": [f.name for f in table.all_fields],
    }


def field_to_schema(field: Field) -> Dict:
    if field.is_relationship:
        assert isinstance(field, Relationship)
        if field.dependent:
            if (
                field.type == "one-to-one"
                or field.type == "many-to-one"
            ):
                return {
                    "$ref": f"#components/schemas/{field.relatedModelName.capitalize()}"
                }
            else:
                return {
                    "type": "array",
                    "items": {
                        "$ref": f"#components/schemas/{field.relatedModelName.capitalize()}"
                    },
                }
        else:
            return {
                "type": "string",
                "description": "A URL for querying information about a related record",
                "example": "/api/specify/"
                + field.relatedModelName.lower()
                + "/3/",
            }

    elif field.type in ("text", "java.lang.String"):
        return {
            "type": required_to_schema(field, "string"),
            "maxLength": getattr(field, "length", 0),
        }

    elif field.type in (
        "java.lang.Integer",
        "java.lang.Long",
        "java.lang.Byte",
        "java.lang.Short",
        "java.lang.Float",
        "java.lang.Double",
    ):
        return {"type": required_to_schema(field, "number")}

    elif field.type in ("java.util.Calendar", "java.util.Date"):
        return {
            "type": required_to_schema(field, "string"),
            "format": "date",
        }

    elif field.type == "java.sql.Timestamp":
        return {
            "type": required_to_schema(field, "string"),
            "format": "date-time",
        }

    elif field.type == "java.math.BigDecimal":
        return {"type": required_to_schema(field, "string")}

    elif field.type == "java.lang.Boolean":
        return {"type": required_to_schema(field, "boolean")}

    else:
        raise Exception(f"unexpected field type: {field.type}")


def required_to_schema(
    field: Field, ftype: str
) -> Union[str, List[str]]:
    return ftype if field.required else [ftype, "null"]
