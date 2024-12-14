
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
from drf_yasg.utils import swagger_auto_schema
import json



response_post = {
    "message": [
        "User created successfully."
    ],
    "code": 201,
    "success": True,
    "data": {
        "first_name": "Mahesh",
        "last_name": "Shukla",
        "email": "mahesh2221@yopmail.com",
        "mobile": 8765644756,
        "username": "mahi2121",
        "is_active": 1,
        "status": 1,
        "role": 3,
        "is_librarian": 0
    }
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
        'User already exists.'
    ],
    'code': 400,
    'success': True,
    'data': {}
}

response_not_found = {
    'message': [
        'User not found'
    ],
    'code': 404,
    'success': True,
    'data': {}
}


swagger_auto_schema_post = swagger_auto_schema(
    responses={
        '201': json.dumps(response_post),
        '400': json.dumps(response_bad_request),
        '401': json.dumps(response_unauthorized),
        '403': json.dumps(response_unauthenticate),
    },

    operation_id='Create Users',
    operation_description='API to add new Users request :: {"first_name":"Laxi","last_name":"Saxena","email":"laxi2121@yopmail.com","mobile":8765644656,"username":"laxi2121","is_active":1,"status":1,"role":3,"is_librarian":0,"password":"123456"}',
)

    