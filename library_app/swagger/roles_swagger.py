from drf_yasg.openapi import Parameter, IN_QUERY
from drf_yasg.utils import swagger_auto_schema
import json

response_list = {
    "message": [
        "Ok"
    ],
    "code": 200,
    "success": True,
    "data": [
        {
            "id": 1,
            "designation": "Super Admin"
        },
    ],
    "paginator": {
        "total_count": 1,
        "total_pages": 1,
        "current_page": 1,
        "limit": 10
    }
}

response_unauthenticate = {
    "message": ["Authentication credentials were not provided."],
    "code": 403,
    "success": True,
    "data": {},
}

response_unauthorized = {"message": ["Unauthorized"], "code": 401, "success": True, "data": {}}

swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter("sort_by", IN_QUERY, description="sort by id", type="int"),
        Parameter(
            "sort_direction", IN_QUERY, description="sort_direction in ascending,descending", type="char"
        ),
        Parameter("id", IN_QUERY, description="id parameter", type="char"),
        Parameter("keyword", IN_QUERY, description="keyword paramater", type="char"),
        Parameter("page", IN_QUERY, description="page no. paramater", type="int"),
        Parameter("limit", IN_QUERY, description="limit paramater", type="int"),
    ],
    responses={
        "200": json.dumps(response_list),
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
    },
    operation_id="list states",
    operation_description="API to list states data",
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        "403": json.dumps(response_unauthenticate),
        "401": json.dumps(response_unauthorized),
    },
    operation_id="Fetch states",
    operation_description="API to fetch states",
)
