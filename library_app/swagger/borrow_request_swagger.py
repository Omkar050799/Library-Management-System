
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
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
            "book_id": 1,
            "title": "Life of Pie",
            "author": "Omkar More",
            "user_id": 7,
            "user_name": "Laxi Saxena",
            "start_date": "2024-12-12",
            "end_date": "2024-12-20",
            "status": "Approved",
            "status_name": 2
        },
        {
            "id": 2,
            "book_id": 2,
            "title": "Journy To The Jumanji",
            "author": "Rakesh Mehra",
            "user_id": 7,
            "user_name": "Laxi Saxena",
            "start_date": "2024-12-21",
            "end_date": "2024-12-23",
            "status": "Approved",
            "status_name": 2
        },
        {
            "id": 3,
            "book_id": 1,
            "title": "Life of Pie",
            "author": "Omkar More",
            "user_id": 6,
            "user_name": "Pihu Mahajan",
            "start_date": "2024-12-23",
            "end_date": "2024-12-25",
            "status": "Approved",
            "status_name": 2
        },
        {
            "id": 4,
            "book_id": 1,
            "title": "Life of Pie",
            "author": "Omkar More",
            "user_id": 5,
            "user_name": "Ramesh Shukla",
            "start_date": "2024-12-01",
            "end_date": "2024-12-02",
            "status": "Pending",
            "status_name": 1
        },
        {
            "id": 5,
            "book_id": 1,
            "title": "Life of Pie",
            "author": "Omkar More",
            "user_id": 5,
            "user_name": "Ramesh Shukla",
            "start_date": "2024-12-03",
            "end_date": "2024-12-04",
            "status": "Pending",
            "status_name": 1
        },
        {
            "id": 6,
            "book_id": 1,
            "title": "Life of Pie",
            "author": "Omkar More",
            "start_date": "2024-12-05",
            "end_date": "2024-12-06",
            "status": "Pending",
            "status_name": 1
        }
    ],
    "paginator": {
        "total_count": 6,
        "total_pages": 1,
        "current_page": 1,
        "limit": 10
    }
}

response_get = {
     "message": [
        "Ok"
    ],
    "code": 200,
    "success": True,
    "data": {
        "id": 1,
        "book_id": 1,
        "title": "Life of Pie",
        "author": "Omkar More",
        "user_id": 7,
        "user_name": "Laxi Saxena",
        "start_date": "2024-12-12",
        "end_date": "2024-12-20",
        "status": "Approved",
        "status_name": 2
    }
}

response_post = {
    "message": [
        "Borrow request stored successfully."
    ],
    "code": 201,
    "success": True,
    "data": {
        "book": 1,
        "start_date": "2024-12-05",
        "end_date": "2024-12-06"
    }
}


response_update = {
     "message": [
        "Borrow request stored successfully."
    ],
    "code": 201,
    "success": True,
    "data": {
        "book": 1,
        "start_date": "2024-12-05",
        "end_date": "2024-12-06"
    }
}

response_delete = {
    'message': [
        'Borrow request deleted'
    ],
    'code': 200,
    'success': True,
    'data': {}
}

response_unauthenticate = {
    'message': [
        "Authentication credentials were not provided."
    ],
    'code': 401,
    'success': True,
    'data': {}
}

response_unauthorized = {
    'message': [
        "You do not have permission to perform this action."
    ],
    'code': 403,
    'success': True,
    'data': {}

}

response_bad_request = {
    'message': [
        'Borrow request already exists.'
    ],
    'code': 400,
    'success': True,
    'data': {}
}

response_not_found = {
    'message': [
        'Borrow request not found'
    ],
    'code': 404,
    'success': True,
    'data': {}
}

swagger_auto_schema_list = swagger_auto_schema(
    manual_parameters=[
        Parameter('sort_by', IN_QUERY, description='sort by id', type='int'),
        Parameter('sort_direction', IN_QUERY, description='sort_direction in ascending,descending', type='char'),
        Parameter('id', IN_QUERY, description='id parameter', type='char'),
        Parameter('keyword', IN_QUERY, description='keyword paramater', type='char'),
        Parameter('page', IN_QUERY, description='page no. paramater', type='int'),
        Parameter('limit', IN_QUERY, description='limit paramater', type='int'),
        Parameter('type', IN_QUERY, description='All result set type=all', type='char'),
        Parameter('book_id', IN_QUERY, description='book paramater', type='int'),
        Parameter('user_id', IN_QUERY, description='user paramater', type='int'),
        Parameter('start_date', IN_QUERY, description='start_date paramater', type='char'),
        Parameter('end_date', IN_QUERY, description='end_date paramater', type='char'),
    ],
    responses={
        '200': json.dumps(response_list),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found)
    },

    operation_id='list Borrow request',
    operation_description='API to list Borrow request data',
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
    },

    operation_id='Create Borrow request',
    operation_description='API to add new Borrow request request :: { "book" : 1, "start_date" : "2024-12-05", "end_date" : "2024-12-06" }',)

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='update Borrow request',
    operation_description='API to update Borrow request request :: { "book" : 1, "start_date" : "2024-12-05", "end_date" : "2024-12-06" }',
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete Borrow request',
    operation_description='API to delete Borrow request',
)

swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete Borrow request',
    operation_description='API to bulk delete Borrow request',
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_get),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found),
    },

    operation_id='Fetch Borrow request',
    operation_description='API to fetch Borrow request',
)
    