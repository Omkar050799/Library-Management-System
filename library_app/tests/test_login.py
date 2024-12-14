from utility.constants import BASE_URL
from utility.constants import *
from ..models import User
from utility.constants import BASE_URL
from utility.test_utility import *

class LoginTest(BaseTestCase):
    model_class = User

    @classmethod
    def setUpTestData(self):
        self.user ,created = self.model_class.objects.get_or_create(
            first_name = "demo",
            last_name = "user",
            email = "demo11@test.com",
            mobile = 9988776655,
            username = "userdemo",
            role_id = SUPER_ADMIN_ROLE,
            )
        self.user.set_password("reset123")
        self.user.save()

        self.inactive_user, created = self.model_class.objects.get_or_create(
            first_name = "user",
            last_name = "demo",
            email = "demo@test.com",
            mobile = 9988336655,
            username = "demo",
            role_id = SUPER_ADMIN_ROLE,
            status = STATUS_INACTIVE
            )
        self.inactive_user.set_password("reset123")
        self.inactive_user.save()
        
        self.deleted_user, created = self.model_class.objects.get_or_create(
            first_name = "demo1",
            last_name = "user2",
            email = "demo22@test.com",
            mobile = 9988771155,
            username = "demouser",
            role_id = SUPER_ADMIN_ROLE,
            status = STATUS_DELETED
            )
        self.deleted_user.set_password("reset123")
        self.deleted_user.save()

    url = BASE_URL + "login/"
        
    data = dict()

    # test login api valid unit test
    def test_add_api_valid(self):
        self.data["username"] = self.user.email
        self.data["password"] = "reset123"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)

    # test login api invalid unit test
    def test_add_api_empty_username(self):
        self.data["username"] = " "
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        
    # test login api invalid unit test
    def test_add_api_invalid_username(self):
        self.data["username"] = "demotest"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 403)
        
    # test login api invalid unit test
    def test_add_api_invalid_password(self):
        self.data["username"] = self.user.email
        self.data["password"] = "123"
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 403)
        
    # test login api invalid unit test
    def test_add_api_invalid_inactive_user(self):
        self.data["username"] = self.inactive_user.email
        self.data["password"] = "reset123" 
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        
    # test login api invalid unit test
    def test_add_api_invalid_deleted_user(self):
        self.data["username"] = self.deleted_user.email
        self.data["password"] = "reset123" 
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)