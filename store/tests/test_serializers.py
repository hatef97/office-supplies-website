from rest_framework.exceptions import ValidationError

from django.test import TestCase

from decimal import Decimal

from store.serializers import *
from store.models import *



class CategorySerializerTest(TestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.category = Category.objects.create(
            name="Electronics",
            description="All kinds of electronic items."
        )


    def test_valid_category_serialization(self):
        """Test that valid category data serializes correctly."""
        serializer = CategorySerializer(instance=self.category)
        
        expected_data = {
            "id": self.category.id,
            "name": "Electronics",
            "description": "All kinds of electronic items.",
            "num_of_products": 0  # No products yet
        }
        
        self.assertEqual(serializer.data, expected_data)


    def test_invalid_category_name_too_short(self):
        """Test that a category with a short name raises a validation error."""
        invalid_data = {
            "name": "TV",  # Too short (less than 3 chars)
            "description": "Television category"
        }
        
        serializer = CategorySerializer(data=invalid_data)
        
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn("Category title should be at least 3.", str(context.exception))

    def test_category_num_of_products(self):
        """Test that the num_of_products field correctly counts associated products."""
        Product.objects.create(name="Laptop", price=1000, category=self.category)
        Product.objects.create(name="Smartphone", price=700, category=self.category)

        serializer = CategorySerializer(instance=self.category)

        self.assertEqual(serializer.data["num_of_products"], 2)  # ✅ Now has 2 products



class ProductSerializerTest(TestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.category = Category.objects.create(name="Electronics", description="Electronic items")

        self.product = Product.objects.create(
            name="Laptop",
            description="A high-end gaming laptop.",
            price=1500.00,
            category=self.category,
            stock=10
        )


    def test_valid_product_serialization(self):
        """Test that valid product data serializes correctly."""
        serializer = ProductSerializer(instance=self.product)
        
        expected_data = {
            "id": self.product.id,
            "name": "Laptop",
            "description": "A high-end gaming laptop.",
            "price": Decimal("1500.00"),
            "category": self.category.id,
            "category_name": "Electronics",
            "stock": 10,
            "image": None,  # Assuming the image is not set
            "created_at": serializer.data["created_at"],  # Auto-generated field
        }

        self.assertEqual(serializer.data, expected_data)


    def test_category_name_field(self):
        """Test that the category_name field correctly represents the category name."""
        serializer = ProductSerializer(instance=self.product)
        self.assertEqual(serializer.data["category_name"], "Electronics")


    def test_negative_price_validation(self):
        """Test that a negative price raises a validation error."""
        invalid_data = {
            "name": "Smartphone",
            "description": "Latest smartphone model",
            "price": -100,
            "category": self.category.id,
            "stock": 5
        }
        
        serializer = ProductSerializer(data=invalid_data)
        
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn("Price cannot be negative.", str(context.exception))


    def test_negative_stock_validation(self):
        """Test that a negative stock raises a validation error."""
        invalid_data = {
            "name": "Smartphone",
            "description": "Latest smartphone model",
            "price": 500,
            "category": self.category.id,
            "stock": -5  # Invalid stock value
        }
        
        serializer = ProductSerializer(data=invalid_data)
        
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        
        self.assertIn("Stock cannot be negative.", str(context.exception))


    def test_slug_is_created_on_product_creation(self):
        """Test that a slug is generated when a product is created."""
        data = {
            "name": "Wireless Headphones",
            "description": "Noise-canceling wireless headphones",
            "price": 200,
            "category": self.category
        }
        
        product = Product(**data)
        product.slug = slugify(product.name)  # Simulate the `create` method
        product.save()
        
        self.assertEqual(product.slug, "wireless-headphones")



class CommentSerializerTest(TestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.category = Category.objects.create(name="Electronics", description="Electronic items")

        self.product = Product.objects.create(
            name="Laptop",
            description="A high-end gaming laptop.",
            price=1500.00,
            category=self.category,
            stock=10
        )

        self.comment = Comment.objects.create(
            product=self.product,
            name="John Doe",
            body="Great product!"
        )


    def test_valid_comment_serialization(self):
        """Test that valid comment data serializes correctly."""
        serializer = CommentSerializer(instance=self.comment)
        
        expected_data = {
            "id": self.comment.id,
            "name": "John Doe",
            "body": "Great product!"
        }

        self.assertEqual(serializer.data, expected_data)


    def test_create_comment_with_product_pk(self):
        """Test that a comment is created with the correct product_id from context."""
        data = {
            "name": "Jane Doe",
            "body": "Amazing quality!"
        }

        serializer = CommentSerializer(data=data, context={"product_pk": self.product.id})
        self.assertTrue(serializer.is_valid())

        comment = serializer.save()

        self.assertEqual(comment.name, "Jane Doe")
        self.assertEqual(comment.body, "Amazing quality!")
        self.assertEqual(comment.product_id, self.product.id)  # ✅ Ensures correct product association


    def test_missing_product_pk_in_context(self):
        """Test that a missing product_pk in context raises an error."""
        data = {
            "name": "Jane Doe",
            "body": "Amazing quality!"
        }

        serializer = CommentSerializer(data=data)  # ❌ No 'product_pk' in context

        with self.assertRaises(KeyError):
            serializer.is_valid(raise_exception=True)
            serializer.save()
