from django.test import TestCase
from django.contrib.auth import get_user_model

from .forms import RegisterUser


class RegisterUserFormTest(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_register_form_rejects_duplicate_email_case_insensitive(self):
        self.User.objects.create_user(username="u1", email="Test@Example.com", password="pass12345")

        form = RegisterUser(
            data={
                "username": "u2",
                "email": "test@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "name": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_register_form_rejects_duplicate_username_case_insensitive(self):
        self.User.objects.create_user(username="Admin", email="a@a.com", password="pass12345")

        form = RegisterUser(
            data={
                "username": "admin",
                "email": "b@b.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
                "name": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
