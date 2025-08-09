from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class CustomUserModelTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="arjun", phone="1234567890", password="password", role="rider"
        )

        self.assertEqual(user.username, "arjun")
        self.assertEqual(user.phone, "1234567890")
        self.assertTrue(user.check_password("password"))
        self.assertEqual(user.role, "rider")

    def test_username_is_unique(self):
        CustomUser.objects.create_user(
            username="arjun",
            phone="1234567890",
            password="password",
        )
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="arjun",
                phone="1234567890",
                password="password",
            )
