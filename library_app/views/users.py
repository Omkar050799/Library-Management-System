from utility.utils import generate_token, get_login_response, get_serielizer_error
from ..model.users import User
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from ..serializers.login_serializer import LoginSerializer
from utility.utils import MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet
from utility.utils import revoke_oauth_token
from utility.response import ApiResponse

from ..swagger.users_swagger import swagger_auto_schema_post, swagger_auto_schema

class ImpersonateView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [OAuth2Authentication, ]
    serializer_class = LoginSerializer
    singular_name = "Login"
    model_class = User.objects

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    """ User impersonate """

    def retrieve(self, request, **kwargs):
        """
        API to impersonate to other user only for admin.
        """
        try:
            id = self.kwargs.get('id')
            
            self.old_user = request.user
            user = self.get_object(id)
            if user:
                """
                Authorize to user
                """
                token = generate_token(request, user)
                resp_dict = get_login_response(user, token)
                
                """LOGOUT OLDUSER"""
                if resp_dict:
                    try:
                        response = revoke_oauth_token(request)
                    except:
                        pass
                return ApiResponse.response_ok(self, data=resp_dict, message="Login successful")

            return ApiResponse.response_ok(self, data=[], message="User not found")
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])

    @swagger_auto_schema_post
    def create(self, request, *args, **kwargs):
        try:
            req_data = request.data.copy()

            email= req_data.get('email')
            first_name= req_data.get('first_name')
            last_name= req_data.get('last_name')
            mobile= req_data.get('mobile')
            password= req_data.get('password')
            is_librarian = req_data.get('is_librarian')

            if check_user_exist := self.model_class.filter(email=email).first():
                return ApiResponse.response_bad_request(self, message="User already exists.")
            
            req_data.pop('password')
            serializer = self.serializer_class(data=req_data)

            if not serializer.is_valid():
                serializer_error = get_serielizer_error(serializer)
                return ApiResponse.response_bad_request(self, message=serializer_error)

            user_instance = serializer.save()
            user_instance.set_password(password)
            user_instance.save()
            
            return ApiResponse.response_created(self, data=req_data, message="User created successfully.")
            
        except Exception as e:
            return ApiResponse.response_internal_server_error(self, message=[str(e.args[0])])
