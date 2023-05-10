from django.test import TestCase
from django.contrib.auth.models import User
from kanban_app.forms import SignUpForm, LoginForm


# More thorough authentication tests are in the test_authentication.py file

class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_credentials = {"username": "created_user", "password": "createdpass123"}
        cls.created_user = User.objects.create_user(
            username=cls.user_credentials["username"], 
            password=cls.user_credentials["password"],
        )


class SignUpFormTest(BaseTest):
    def test_valid_form(self):
        data = {"username": "test_user", "password1": "testpass123", "password2": "testpass123"}
        form = SignUpForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        data = {"username": "", "password1": "testpass123", "password2": "testpass123"}
        form = SignUpForm(data=data)
        self.assertFalse(form.is_valid())


class LoginFormTest(BaseTest):
    def test_valid_form(self):
        data = {"username": self.user_credentials["username"], "password": self.user_credentials["password"]}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_data(self):
        data = {"username": "", "password": self.user_credentials["password"]}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
