
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
            "title": "Life of Pie",
            "author": "Omkar More"
        },
        {
            "id": 2,
            "title": "Journy To The Jumanji",
            "author": "Rakesh Mehra"
        }
    ],
    "paginator": {
        "total_count": 2,
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
        "title": "Life of Pie",
        "author": "Omkar More"
    }
}

response_post = {
   "message": [
        "Books details stored successfully."
    ],
    "code": 201,
    "success": True,
    "data": {
        "title": "Moons",
        "author": "Marie Jain",
        "isbn": "212124",
        "copies_available": 3
    }
}


response_update = {
    "message": [
        "Books details update successfully."
    ],
    "code": 201,
    "success": True,
    "data": {
        "title": "Moons",
        "author": "Marie Jain",
        "isbn": "212124",
        "copies_available": 3
    }
}

response_delete = {
    'message': [
        'Book deleted'
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
        'Book already exists.'
    ],
    'code': 400,
    'success': True,
    'data': {}
}

response_not_found = {
    'message': [
        'Book not found'
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
        Parameter('start_date', IN_QUERY, description='start_date paramater', type='char'),
        Parameter('end_date', IN_QUERY, description='end_date paramater', type='char'),
    ],
    responses={
        '200': json.dumps(response_list),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found)
    },

    operation_id='list books',
    operation_description='API to list books data',
)

swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
    },

    operation_id='Create books',
    operation_description='API to add new books request :: {"title": "Journy To The Jumanji","author": "Rakesh Mehra,","isbn" : "212121","copies_available":3    }',)

swagger_auto_schema_update = swagger_auto_schema(
    responses={
        '200': json.dumps(response_update),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='update books',
    operation_description='API to update books request :: {"title": "Journy To The Jumanji","author": "Rakesh Mehra,","isbn" : "212121","copies_available":3    }',
)

swagger_auto_schema_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete books',
    operation_description='API to delete books',
)

swagger_auto_schema_bulk_delete = swagger_auto_schema(
    responses={
        '200': json.dumps(response_delete),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
        '404': json.dumps(response_not_found),
    },

    operation_id='delete books',
    operation_description='API to bulk delete books',
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        '200': json.dumps(response_get),
        '403': json.dumps(response_unauthenticate),
        '401': json.dumps(response_unauthorized),
        '404': json.dumps(response_not_found),
    },

    operation_id='Fetch books',
    operation_description='API to fetch books',
)
    