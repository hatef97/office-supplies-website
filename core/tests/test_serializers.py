from django.test import TestCase
from django.contrib.auth import get_user_model

from core.serializers import UserCreateSerializer, UserSerializer

from rest_framework.exceptions import ValidationError



User = get_user_model()



class UserCreateSerializerTest(TestCase):

    def setUp(self):
        """Set up test user."""
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword123',
            'first_name': 'John',
            'last_name': 'Doe'
        }


    def test_valid_user_creation_serialization(self):
        """Test that valid user data serializes correctly."""
        serializer = UserCreateSerializer(data=self.valid_user_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['username'], self.valid_user_data['username'])
        self.assertEqual(validated_data['email'], self.valid_user_data['email'])
        self.assertEqual(validated_data['first_name'], self.valid_user_data['first_name'])
        self.assertEqual(validated_data['last_name'], self.valid_user_data['last_name'])


    def test_missing_required_fields(self):
        """Test that missing fields raise validation errors."""
        invalid_data = {
            'username': '',
            'email': '',
            'password': '',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        serializer = UserCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertIn('email', serializer.errors)
        self.assertIn('password', serializer.errors)
