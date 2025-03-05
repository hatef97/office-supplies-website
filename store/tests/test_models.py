from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
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



class DiscountModelTest(TestCase):

    def setUp(self):
        self.discount = Discount.objects.create(
            discount=10.5,
            description="Spring Sale"
        )

    def test_discount_creation(self):
        """Test if a Discount instance is created correctly."""
        self.assertEqual(self.discount.discount, 10.5)
        self.assertEqual(self.discount.description, "Spring Sale")

    def test_discount_float_field(self):
        """Test if discount field accepts float values correctly."""
        self.discount.discount = 15.75
        self.discount.save()
        self.assertEqual(self.discount.discount, 15.75)

    def test_description_max_length(self):
        """Test if description has a maximum length of 255 characters."""
        max_length = Discount._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)

    def test_string_representation(self):
        """Optionally, if you want to add a __str__ method to Discount, you could test it like this."""
        self.discount.description = "Holiday Discount"
        self.discount.save()



class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="All kinds of electronics"
        )

        self.discount1 = Discount.objects.create(
            discount=10.0,
            description="Spring Sale"
        )

        self.discount2 = Discount.objects.create(
            discount=15.0,
            description="Holiday Discount"
        )

        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone with high specs",
            price=599.99,
            category=self.category,
            stock=50,
            created_at=now(),
        )

        self.product.discounts.add(self.discount1, self.discount2)

    def test_product_creation(self):
        """Test product instance is created correctly."""
        self.assertEqual(self.product.name, "Smartphone")
        self.assertEqual(self.product.description, "Latest smartphone with high specs")
        self.assertEqual(self.product.price, 599.99)
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.stock, 50)

    def test_string_representation(self):
        """Test the __str__ method of Product."""
        self.assertEqual(str(self.product), "Smartphone")

    def test_category_relationship(self):
        """Test that product is linked to the correct category."""
        self.assertEqual(self.product.category.name, "Electronics")

    def test_discounts_relationship(self):
        """Test the many-to-many relationship with Discount."""
        discounts = self.product.discounts.all()
        self.assertEqual(discounts.count(), 2)
        self.assertIn(self.discount1, discounts)
        self.assertIn(self.discount2, discounts)

    def test_image_field_blank(self):
        """Test that image field can be left blank."""
        self.assertFalse(self.product.image)

    def test_image_upload(self):
        """Test uploading an image to the product."""
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        self.product.image = image
        self.product.save()
        self.assertTrue(self.product.image.name.startswith('products/test_image'))

    def test_default_stock(self):
        """Test stock default value."""
        product_without_stock = Product.objects.create(
            name="Tablet",
            description="High performance tablet",
            price=299.99,
            category=self.category
        )
        self.assertEqual(product_without_stock.stock, 0)

    def test_created_at_auto_now_add(self):
        """Test created_at is set on creation."""
        self.assertIsNotNone(self.product.created_at)
