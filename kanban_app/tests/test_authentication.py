from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.authentication_url = reverse("index")
        cls.authentication_template = "index.html"
        cls.success_redirect_url = reverse("board")
        created_user = User.objects.create_user(username="created_user", password="createdpass123")
        cls.signup_user = {
            "submit": "signup_form",
            "username": "test_user", 
            "password1": "testpass123",
            "password2": "testpass123",
        }
        cls.signup_user_invalid_username = {
            "submit": "signup_form",
            "username": "invalid test user", 
            "password1": "testpass123",
            "password2": "testpass123",
        }
        cls.signup_user_taken_username = {
            "submit": "signup_form",
            "username": created_user.username, 
            "password1": "testpass123",
            "password2": "testpass123",
        }
        cls.signup_user_short_password = {
            "submit": "signup_form",
            "username": "test_user", 
            "password1": "short",
            "password2": "short",
        }
        cls.signup_user_passwords_not_matching = {
            "submit": "signup_form",
            "username": "test_user", 
            "password1": "testpass123",
            "password2": "123passtest",
        }
        cls.login_user = {
            "submit": "login_form",
            "username": created_user.username, 
            "password": "createdpass123",
        }
        cls.login_user_incorrect_username = {
            "submit": "login_form",
            "username": "incorrect_username", 
            "password": "createdpass123",
        }
        cls.login_user_incorrect_password = {
            "submit": "login_form",
            "username": created_user.username, 
            "password": "incorrect_password",
        }
    

class SignupTest(BaseTest):
    def test_signup_success(self):
        response = self.client.post(self.authentication_url, self.signup_user)
        self.assertRedirects(response, self.success_redirect_url, status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_signup_failure_invalid_username(self):
        response = self.client.post(self.authentication_url, self.signup_user_invalid_username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.authentication_template)

    def test_signup_failure_taken_username(self):
        response = self.client.post(self.authentication_url, self.signup_user_taken_username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.authentication_template)

    def test_signup_failure_short_password(self):
        response = self.client.post(self.authentication_url, self.signup_user_short_password)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.authentication_template)

    def test_signup_failure_passwords_not_matching(self):
        response = self.client.post(self.authentication_url, self.signup_user_passwords_not_matching)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.authentication_template)


class LoginTest(BaseTest):
    def test_login_success(self):
        response = self.client.post(self.authentication_url, self.login_user)
        self.assertRedirects(response, self.success_redirect_url, status_code=302, target_status_code=200, fetch_redirect_response=True)

    def test_login_failure_incorrect_username(self):
        response = self.client.post(self.authentication_url, self.login_user_incorrect_username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.authentication_template)

    def test_login_failure_incorrect_password(self):
        response = self.client.post(self.authentication_url, self.login_user_incorrect_password)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.authentication_template)
