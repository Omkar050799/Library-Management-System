from rest_framework import serializers
from ..model.users import User

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
           "first_name", 
           "last_name", 
           "mobile", 
           "status", 
           "role", 
           "is_librarian", 
           "is_active", 
           "is_staff"
        ]
