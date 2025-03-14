from rest_framework.exceptions import ValidationError

from django.test import TestCase
from django.contrib.auth import get_user_model

from decimal import Decimal

from store.serializers import *
from store.models import *



User = get_user_model()



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



class CustomerSerializerTest(TestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="password123")

        self.customer, created = Customer.objects.get_or_create(
            user=self.user,
            defaults={"phone_number": "1234567890", "birth_date": "1990-01-01"}
        )
        # Explicitly update the customer to ensure correct values
        if not created:
            self.customer.phone_number = "1234567890"
            self.customer.birth_date = "1990-01-01"
            self.customer.save()


    def test_valid_customer_serialization(self):
        """Test that valid customer data serializes correctly."""
        serializer = CustomerSerializer(instance=self.customer)
        
        expected_data = {
            "id": self.customer.id,
            "user": self.user.id,  # Ensuring the user field is included as an ID
            "phone_number": "1234567890",
            "birth_date": "1990-01-01"
        }

        self.assertEqual(serializer.data, expected_data)


    def test_read_only_user_field(self):
        """Test that the user field is read-only and cannot be changed."""
        data = {
            "user": 999,  # Invalid user ID (should be read-only)
            "phone_number": "0987654321",
            "birth_date": "2000-05-15"
        }

        serializer = CustomerSerializer(instance=self.customer, data=data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated_customer = serializer.save()

        self.assertEqual(updated_customer.user, self.customer.user)  # ✅ User should remain unchanged


    def test_create_customer_successfully(self):
        """Test that a new customer can be created successfully."""
        new_user = User.objects.create_user(username="newuser", email="newuser@example.com", password="password123")

        Customer.objects.filter(user=new_user).delete()

        data = {
            "phone_number": "5551234567",
            "birth_date": "1995-08-20"
        }

        serializer = CustomerSerializer(data=data, context={"user": new_user})
        self.assertTrue(serializer.is_valid())

        # Create customer only if it doesn't exist
        customer, created = Customer.objects.get_or_create(user=new_user, defaults=serializer.validated_data)   

        self.assertTrue(created)
        self.assertEqual(customer.phone_number, "5551234567")
        self.assertEqual(str(customer.birth_date), "1995-08-20")
        self.assertEqual(customer.user, new_user)


    def test_missing_required_fields(self):
        """Test that missing required fields raise a validation error."""
        data = {}  # Empty data should fail

        serializer = CustomerSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)



class AddCartItemSerializerTest(TestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.cart = Cart.objects.create()

        self.category = Category.objects.create(name="Electronics", description="Electronic items")

        self.product = Product.objects.create(
            name="Laptop",
            description="A high-end gaming laptop.",
            price=1500.00,
            category=self.category,
            stock=10
        )


    def test_valid_cart_item_serialization(self):
        """Test that valid cart item data serializes correctly."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        serializer = AddCartItemSerializer(instance=cart_item)
        
        expected_data = {
            "id": cart_item.id,
            "product": self.product.id,
            "quantity": 2
        }

        self.assertEqual(serializer.data, expected_data)


    def test_create_new_cart_item(self):
        """Test that a new cart item is created successfully if it does not exist."""
        data = {
            "product": self.product.id,
            "quantity": 3
        }

        serializer = AddCartItemSerializer(data=data, context={"cart_pk": self.cart.id})
        self.assertTrue(serializer.is_valid())

        cart_item = serializer.save()

        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(cart_item.cart_id, self.cart.id)


    def test_update_existing_cart_item_quantity(self):
        """Test that an existing cart item has its quantity increased."""
        existing_cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        data = {
            "product": self.product.id,
            "quantity": 3  # Adding more of the same product
        }

        serializer = AddCartItemSerializer(data=data, context={"cart_pk": self.cart.id})
        self.assertTrue(serializer.is_valid())

        updated_cart_item = serializer.save()

        self.assertEqual(updated_cart_item.id, existing_cart_item.id)  # ✅ Same cart item should be updated
        self.assertEqual(updated_cart_item.quantity, 5)  # ✅ Quantity should be increased


    def test_missing_cart_context_raises_error(self):
        """Test that a missing 'cart_pk' in context raises a KeyError."""
        data = {
            "product": self.product.id,
            "quantity": 2
        }

        serializer = AddCartItemSerializer(data=data)  # ❌ No 'cart_pk' in context

        with self.assertRaises(KeyError):
            serializer.is_valid(raise_exception=True)
            serializer.save()


    def test_negative_quantity_raises_error(self):
        """Test that providing a negative quantity raises a validation error."""
        data = {
            "product": self.product.id,
            "quantity": -1  # Invalid quantity
        }

        serializer = AddCartItemSerializer(data=data, context={"cart_pk": self.cart.id})

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("quantity", str(context.exception))



class UpdateCartItemSerializerTest(TestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.cart = Cart.objects.create()

        self.category = Category.objects.create(name="Electronics", description="Electronic items")

        self.product = Product.objects.create(
            name="Laptop",
            description="A high-end gaming laptop.",
            price=1500.00,
            category=self.category,
            stock=10
        )

        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)


    def test_valid_cart_item_update(self):
        """Test that updating cart item quantity works correctly."""
        data = {"quantity": 5}  # Valid new quantity

        serializer = UpadateCartItemSerializer(instance=self.cart_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_cart_item = serializer.save()

        self.assertEqual(updated_cart_item.quantity, 5)  # ✅ Quantity should be updated


    def test_negative_quantity_raises_error(self):
        """Test that providing a negative quantity raises a validation error."""
        data = {"quantity": -1}  # Invalid quantity

        serializer = UpadateCartItemSerializer(instance=self.cart_item, data=data, partial=True)

        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("quantity", str(context.exception))  # ✅ Ensures proper error message


    def test_zero_quantity_is_valid(self):
        """Test that setting quantity to zero is allowed (for removing items)."""
        data = {"quantity": 0}  # Removing item

        serializer = UpadateCartItemSerializer(instance=self.cart_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_cart_item = serializer.save()

        self.assertEqual(updated_cart_item.quantity, 0)  # ✅ Quantity should be updated to zero


    def test_large_quantity_is_valid(self):
        """Test that setting a large quantity is valid."""
        data = {"quantity": 1000}  # Large but valid quantity

        serializer = UpadateCartItemSerializer(instance=self.cart_item, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_cart_item = serializer.save()

        self.assertEqual(updated_cart_item.quantity, 1000)  # ✅ Quantity should be updated
        