from drf_yasg.utils import swagger_auto_schema
import json

login = {
    "message": [
        "Login successful"
    ],
    "code": 200,
    "success": True,
    "data": {
        "id": 1,
        "first_name": "super",
        "last_name": "admin",
        "email": "library_management@yopmail.com",
        "mobile": "9119533042",
        "username": "super@gmail.com",
        "token": {
            "access_token": "MKIEomHhRSIQhdDJRSwZeqa5wA0bIa",
            "token_type": "Bearer",
            "expires_in": 36000,
            "refresh_token": "AHl2vKFmrTG4BzwEX5Xy922CFM8Ak2",
            "scope": {
                "read": "Read scope"
            }
        }
    }
}

invalid_login = {
    "message": [
        "Invalid username or password. Please try again."
    ],
    "code": 403,
    "success": False,
    "data": {}
}

logout = {
    "message": [
        "Logout successful"
    ],
    "code": 200,
    "success": True,
    "data": []
}

swagger_auto_schema_logout = swagger_auto_schema(
    responses={
        "200": json.dumps(logout),
    },
    operation_id="logout ",
    operation_description="API to logout",
)

swagger_auto_schema = swagger_auto_schema(
    responses={
        "200": json.dumps(login),
        "403": json.dumps(invalid_login),
    },
    operation_id="login",
    operation_description='API to login \n \n request::   {"email": "library_management@yopmail.com","password": "123456"}')
