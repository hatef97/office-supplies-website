from django.test import TestCase
from django.db.utils import IntegrityError

from core.models import CustomUser



class CustomUserModelTest(TestCase):

    def setUp(self):
        """Set up test users."""
        self.user1 = CustomUser.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password123"
        )


    def test_create_user(self):
        """Test creating a user with email and password."""
        user = CustomUser.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password456"
        )
        self.assertEqual(user.username, "user2")
        self.assertEqual(user.email, "user2@example.com")
        self.assertTrue(user.check_password("password456"))


    def test_email_is_unique(self):
        """Test that email field must be unique."""
        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="duplicate_user",
                email="user1@example.com",  # ❌ Duplicate email
                password="newpassword"
            )


    def test_string_representation(self):
        """Test the string representation of the user."""
        self.assertEqual(str(self.user1), self.user1.username)


    def test_superuser_creation(self):
        """Test creating a superuser."""
        admin_user = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


    def test_user_default_flags(self):
        """Test default flags for a new user."""
        self.assertFalse(self.user1.is_staff)
        self.assertFalse(self.user1.is_superuser)
