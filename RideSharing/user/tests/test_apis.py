from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from user.models import CustomUser


class AuthViewTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("create_user")
        self.login_url = reverse("token_obtain_pair")
        self.logout_url = reverse("user_logout")

        self.user_data = {
            "username": "arjun",
            "phone": "1234567890",
            "password": "password",
            "role": "rider",
        }

        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_register_user(self):
        data = {
            "username": "arjunvjn",
            "phone": "1234567890",
            "password": "password",
            "role": "rider",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "Success")
        self.assertEqual(response.data["data"]["username"], "arjunvjn")

    def test_login(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        self.access_token = response.data["access"]
        self.refresh_token = response.data["refresh"]

    def test_logout(self):
        login_response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        refresh = login_response.data["refresh"]
        access = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        logout_response = self.client.post(
            self.logout_url, {"refresh_token": refresh}, format="json"
        )

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_response.data["status"], "Success")

    def test_register_user_missing_role(self):
        data = {"username": "arun", "phone": "1234567890", "password": "password"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "Error")
        self.assertEqual(response.data["message"], "Role field is required")

    def test_token_refresh(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )

        refresh_token = response.data["refresh"]

        refresh_response = self.client.post(
            reverse("token_refresh"), {"refresh": refresh_token}, format="json"
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)
