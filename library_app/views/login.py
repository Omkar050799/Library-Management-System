from rest_framework.generics import GenericAPIView
from django.db.models import Q
from utility.utils import generate_token, get_login_response
from utility.response import ApiResponse
from utility.constants import MESSAGES, STATUS_ACTIVE, STATUS_INACTIVE  

"""serializer"""
from ..serializers.login_serializer import LoginSerializer

"""Model"""
from ..models import EmailOrUsernameModelBackend, User

"""swagger"""
from ..swagger.login_logout_swagger import swagger_auto_schema


class LoginViewSet(GenericAPIView, ApiResponse, EmailOrUsernameModelBackend):
    serializer_class = LoginSerializer

    @swagger_auto_schema
    def post(self, request, *args, **kwargs):
        """
        API to get logged In.
        """
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return ApiResponse.response_bad_request(self, message=MESSAGES['username_password_required'])

        """ authenticate user and generate token """
        
        try:
            user = User.objects.get(Q(Q(username=username) | Q(email=username)))
            if not user.check_password(password):
                return ApiResponse.response_unauthorized(self, message=MESSAGES['invalid_username_and_password'])

        except User.DoesNotExist as e:
            return ApiResponse.response_unauthorized(self, message=MESSAGES['username_not_exist'])

        if user.status == STATUS_INACTIVE:
            return ApiResponse.response_bad_request(self, message=MESSAGES['user_inactive'])
        
        if user.status != STATUS_ACTIVE:
            return ApiResponse.response_bad_request(self, message=MESSAGES['user_deleted'])
        """
        Authorize to user
        """
        token = generate_token(request, user)
        resp_dict = get_login_response(user, token)
        resp_dict["token"] = token  
        return ApiResponse.response_ok(self, data=resp_dict, message="Login successful")