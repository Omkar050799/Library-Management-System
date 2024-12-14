from random import randint
from oauth2_provider.models import AccessToken
from django.utils import timezone
import django.utils.timezone
from django.utils.timezone import timedelta
import random
import string
from faker import Faker
from oauthlib.common import generate_token
from django.conf import settings
from library_app.models import *
from utility.constants import *
from django.test import TestCase

def get_auth_dict(user):
	expires = timezone.now() + timedelta(
	    seconds=settings.OAUTH2_PROVIDER.get("ACCESS_TOKEN_EXPIRE_SECONDS", 3600)
	)
	access_token = AccessToken.objects.get_or_create(
	    user=user, expires=expires, token=generate_token()
	)
	auth_headers = {
        "HTTP_AUTHORIZATION": "Bearer " + access_token[0].token,
        "HTTP_ACCESS_KEY": ACCESS_KEY,
        "content_type": "application/json",
    }

	return auth_headers
	
def create_user_role():
    role_instance = Roles.objects.create(id=1, name=SUPERUSER_ROLE)
    # Roles.objects.create(id=2, name=AGENT_ROLE)
    # Roles.objects.create(id=3, name=CLIENT_ROLE)
    # Roles.objects.create(id=4, name=SUPER_ADMIN_ROLE)
    return role_instance.id

def random_string_generator(stringLength=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(stringLength))

def random_email_generator():
    fake = Faker()
    return fake.email()

def create_user(role, status=1):
    user, created = User.objects.get_or_create(
        first_name=random_string_generator(),
        email=random_email_generator(),
        mobile=str(randint(100000, 999999999)),
        role_id=role,
        status=status,
    )

    return user

class BaseTestCase(TestCase):
    fixtures = ['fixtures/oauth_provider.json','fixtures/library_management.json']