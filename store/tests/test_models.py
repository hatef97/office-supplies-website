from django.test import TestCase
from django.contrib.auth import get_user_model
from store.models import *
from decimal import Decimal

User = get_user_model()



class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="All kinds of electronic items."
        )

    def test_category_creation(self):
        """Test if a Category instance is created correctly."""
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.description, "All kinds of electronic items.")

    def test_string_representation(self):
        """Test the __str__ method of Category."""
        self.assertEqual(str(self.category), "Electronics")

    def test_name_uniqueness(self):
        """Test that the name field must be unique."""
        with self.assertRaises(Exception):  
            Category.objects.create(name="Electronics", description="Duplicate name test")

    def test_description_blank(self):
        """Test that description can be left blank."""
        category = Category.objects.create(name="Books")
        self.assertEqual(category.description, "")  # Should default to blank
