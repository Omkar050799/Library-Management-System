import requests
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.generics import GenericAPIView
from utility.utils import revoke_oauth_token
from ..serializers.login_serializer import LoginSerializer
from utility.response import ApiResponse
from library_app.swagger.login_logout_swagger import swagger_auto_schema_logout, swagger_auto_schema

class LogoutView(GenericAPIView, ApiResponse):
    serializer_class = LoginSerializer
    authentication_classes = [OAuth2Authentication, ]

    @swagger_auto_schema
    def get(self, request, *args, **kwargs):
        """
        API to logout user.
        """
        try:
            # capture data
            response = revoke_oauth_token(request)
            return ApiResponse.response_ok(self, message="Logout successful", data=response)
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
