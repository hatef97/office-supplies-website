from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from store.models import *

from decimal import Decimal
from datetime import date




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



class CustomerModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="johndoe",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            password="testpassword123"
        )

        Customer.objects.filter(user=self.user).delete()

        self.customer = Customer.objects.create(
            user=self.user,
            phone_number="123-456-7890",
            birth_date=date(1990, 5, 20)
        )


    def test_customer_creation(self):
        """Test customer instance is created correctly."""
        self.assertEqual(self.customer.user, self.user)
        self.assertEqual(self.customer.phone_number, "123-456-7890")  # Check the phone number
        self.assertEqual(self.customer.birth_date, date(1990, 5, 20))

    def test_string_representation(self):
        """Test the __str__ method of Customer."""
        self.assertEqual(str(self.customer), "John Doe")

    def test_full_name_property(self):
        """Test the full_name property."""
        self.assertEqual(self.customer.full_name, "John Doe")

    def test_birth_date_can_be_blank(self):
        """Test birth_date can be blank or null."""
        Customer.objects.filter(user=self.user).delete()
        customer_without_birth_date = Customer.objects.create(
            user=self.user,
            phone_number="999-999-9999"
        )
        self.assertIsNone(customer_without_birth_date.birth_date)

    def test_custom_permission_exists(self):
        """Test that the custom permission 'send_private_email' is correctly defined."""
        permission = Customer._meta.permissions
        self.assertIn(('send_private_email', 'Can send private email to user by the button'), permission)



class OrderModelTest(TestCase):

    def setUp(self):
        # Create a user and customer for the order
        self.user = User.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='testpassword123'
        )
        Customer.objects.filter(user=self.user).delete()
        self.customer = Customer.objects.create(
            user=self.user,
            phone_number="123-456-7890"
        )

        # Create an order instance
        self.order = Order.objects.create(
            customer=self.customer,
            status=Order.ORDER_STATUS_UNPAID
        )

    def test_order_creation(self):
        """Test that an Order instance is created correctly."""
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.status, Order.ORDER_STATUS_UNPAID)
        self.assertIsNotNone(self.order.datetime_created)

    def test_order_status_choices(self):
        """Test that status choices are correctly stored."""
        self.order.status = Order.ORDER_STATUS_PAID
        self.order.save()
        self.assertEqual(self.order.status, Order.ORDER_STATUS_PAID)

        self.order.status = Order.ORDER_STATUS_CANCELED
        self.order.save()
        self.assertEqual(self.order.status, Order.ORDER_STATUS_CANCELED)

    def test_order_default_status(self):
        """Test that the default order status is 'unpaid'."""
        new_order = Order.objects.create(customer=self.customer)
        self.assertEqual(new_order.status, Order.ORDER_STATUS_UNPAID)
