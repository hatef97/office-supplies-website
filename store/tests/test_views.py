from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils.timezone import now

from store.models import *
from store.serializers import CustomerSerializer, CartItemSerializer, OrderSerializer




User = get_user_model()



class ProductViewSetTest(APITestCase):

    def setUp(self):
        
        self.client = APIClient()
        # Create admin and regular user
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        # Authenticate admin user
        self.client.force_authenticate(user=self.admin_user)
        
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
        )
        self.client = APIClient() 
        # Create a category and product 
        self.category = Category.objects.create(name="Stationery")

        self.product = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone with high specs",
            price=599.99,
            category=self.category,
            stock=50,
            created_at=now(),
        )

        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse("product-detail", kwargs={"pk": self.product.id})
    
    
    def test_list_products(self):
        response = self.client.get(self.product_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # Pagination response
    
    
    def test_retrieve_product(self):
        """Test retrieving a single product."""
        response = self.client.get(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_admin_can_create_product(self):
        """Test that an admin user can create a product"""
        self.client.login(username="admin", password="adminpass")  # ✅ Authenticate Admin

        product_data = {
            "name": "New Product",
            "description": "A test product",
            "price": 19.99,
            "category": self.category.id,  # ✅ Pass category ID
            "stock": 10,
        }

        response = self.client.post(self.product_list_url, product_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # ✅ Expect success


    def test_admin_can_update_product(self):
        """✅ Admin user can update a product."""
        self.client.login(username="admin", password="adminpass")  # ✅ Authenticate Admin

        update_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 59.99,
            "category": self.category.id,
            "stock": 5,
        }

        response = self.client.put(self.product_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], update_data["name"])


    def test_admin_can_delete_product(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


    def test_regular_user_cannot_create_product(self):
        """❌ Regular (non-admin) user cannot create a product."""
        self.client.force_authenticate(user=self.regular_user)

        product_data = {
            "name": "Forbidden Product",
            "description": "A test product",
            "price": 19.99,
            "category": self.category.id,
            "stock": 10,
        }


    def test_regular_user_cannot_update_product(self):
        """❌ Regular (non-admin) user cannot update a product."""
        self.client.force_authenticate(user=self.regular_user)

        update_data = {
            "name": "Unauthorized Update",
            "description": "Updated Description",
            "price": 59.99,
            "category": self.category.id,
            "stock": 5,
        }

        response = self.client.put(self.product_detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_regular_user_cannot_delete_product(self):
        self.client.login(username='regular', password='regularpass123')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_unauthenticated_user_cannot_create_product(self):
        """❌ Unauthenticated user cannot create a product."""
        product_data = {
            "name": "Unauthorized Product",
            "description": "A test product",
            "price": 19.99,
            "category": self.category.id,
            "stock": 10,
        }

        response = self.client.post(self.product_list_url, product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_unauthenticated_user_cannot_delete_product(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_search_products_by_name(self):
        """✅ Search products by name."""
        response = self.client.get(f"{self.product_list_url}?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_order_products_by_price(self):
        """✅ Order products by price."""
        response = self.client.get(f"{self.product_list_url}?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class CategoryViewSetTest(APITestCase):

    def setUp(self):
        """Set up test data."""
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        self.regular_user = User.objects.create_user('user', 'user@test.com', 'password')

        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Books")

        self.category_list_url = reverse('category-list')
        self.category_detail_url = reverse('category-detail', kwargs={'pk': self.category1.pk})


    def test_list_categories(self):
        """✅ Test retrieving the list of categories."""
        response = self.client.get(self.category_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)


    def test_retrieve_category(self):
        """✅ Test retrieving a single category."""
        response = self.client.get(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category1.name)


    def test_admin_can_create_category(self):
        """✅ Test that an admin user can create a category."""
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "Fashion"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Category.objects.filter(name="Fashion").exists())


    def test_non_admin_cannot_create_category(self):
        """❌ Test that a regular user cannot create a category."""
        self.client.force_authenticate(user=self.regular_user)
        data = {"name": "Fashion"}
        response = self.client.post(self.category_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_admin_can_update_category(self):
        """✅ Test that an admin user can update a category."""
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "Updated Electronics"}
        response = self.client.put(self.category_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, "Updated Electronics")


    def test_non_admin_cannot_update_category(self):
        """❌ Test that a regular user cannot update a category."""
        self.client.force_authenticate(user=self.regular_user)
        data = {"name": "Updated Electronics"}
        response = self.client.put(self.category_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_cannot_delete_category_with_products(self):
        """❌ Test that a category with products cannot be deleted."""
        Product.objects.create(name="Laptop", category=self.category1, price=1000, stock=10)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertIn('Cannot delete category with existing products. Remove products first.', response.data['error'])


    def test_admin_can_delete_empty_category(self):
        """✅ Test that an admin user can delete a category without products."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category1.pk).exists())


    def test_non_admin_cannot_delete_category(self):
        """❌ Test that a regular user cannot delete a category."""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.category_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class CommentViewSetTest(APITestCase):
    def setUp(self):
        """Set up test dependencies"""
        # Create users with unique emails
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='adminpass'
        )
        self.regular_user = User.objects.create_user(
            username='user', email='user@example.com', password='userpass'
        )
        
        # Create a category
        self.category = Category.objects.create(name="Office Supplies")
        
        # Create a product with a valid category
        self.product = Product.objects.create(
            name="Test Product",
            price=50.0,
            stock=10,
            category=self.category  # ✅ Assign a valid category
        )

        # Create comments
        self.comment = Comment.objects.create(
            product=self.product, name=self.regular_user, body="Great product!"
        )

        # Set URLs
        self.comment_list_url = reverse('product-comments-list', kwargs={'product_pk': self.product.pk})
        self.comment_detail_url = reverse('product-comments-detail', kwargs={'product_pk': self.product.pk, 'pk': self.comment.pk})
        
        
    def test_list_comments(self):
        """Test listing comments for a product"""
        self.client.force_authenticate(user=self.regular_user)
        
        response = self.client.get(self.comment_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one comment exists
        self.assertEqual(response.data[0]['body'], "Great product!")  # Check content


    def test_create_comment_authenticated_user(self):
        """Test that an authenticated user can create a comment"""
        self.client.force_authenticate(user=self.regular_user)

        data = {
                "name": "Test Comment",  
                "body": "This is a test comment",
                "product": self.product.id  
            }
        response = self.client.post(self.comment_list_url, data, format="json")

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)  # Should have 2 comments now


    def test_create_comment_unauthenticated_user(self):
        """Test that an unauthenticated user cannot create a comment"""
        response = self.client.post(self.comment_list_url, {"body": "Not logged in!"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should return 401


    def test_admin_can_delete_comment(self):
        """Test that an admin can delete a comment"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.comment_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)  # Comment should be deleted


    def test_regular_user_cannot_delete_comment(self):
        """Test that a regular user cannot delete a comment"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.comment_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular user cannot delete comments
        self.assertEqual(Comment.objects.count(), 1)  # Comment should still exist


    def test_unauthenticated_user_cannot_delete_comment(self):
        """Test that an unauthenticated user cannot delete a comment"""
        response = self.client.delete(self.comment_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should return 401
        self.assertEqual(Comment.objects.count(), 1)  # Comment should still exist  



class CustomerViewSetTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()

        # Clear old data before each test
        User.objects.all().delete()
        Customer.objects.all().delete()

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )

        # Create regular customer user
        self.customer_user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='password'
        )

        # Create the Customer first
        self.customer, created = Customer.objects.get_or_create(
            user=self.customer_user
        )

        # Set URLs
        self.customer_list = reverse('customer-list')
        self.customer_me = reverse('customer-me')
        self.customer_send_private_email = reverse('customer-send-private-email', args=[self.customer.pk])
            
    def test_me_get_authenticated(self):
        """Test that an authenticated user can retrieve their customer profile."""
        self.client.force_authenticate(user=self.customer_user)

        response = self.client.get(self.customer_me)

        # Ensure request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure the response contains customer data
        self.assertEqual(response.data["user"], self.customer_user.id)
        self.assertEqual(response.data["phone_number"], self.customer.phone_number)
        self.assertEqual(response.data["birth_date"], str(self.customer.birth_date) if self.customer.birth_date else None)

    def test_me_put_authenticated(self):
        """Test that an authenticated user can update their customer profile."""
        url = reverse('customer-me')
        self.client.force_authenticate(user=self.customer_user)

        # New data
        updated_data = {
            "phone_number": "987-654-3210",
            "birth_date": "1995-05-15"
        }

        # Send PUT request
        response = self.client.put(url, updated_data)

        # Ensure request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh customer from database
        self.customer.refresh_from_db()

        # Assert changes
        self.assertEqual(self.customer.phone_number, "987-654-3210")
        self.assertEqual(str(self.customer.birth_date), "1995-05-15")


    def test_me_unauthenticated(self):
        """Test that an unauthenticated user cannot access 'me' endpoint."""
        self.client.logout()
        response = self.client.get(self.customer_me)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    
    def test_send_private_email_permission(self):
        """Test that only users with SendPrivateEmailToCustomerPermission can call send_private_email action."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.customer_send_private_email)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Assuming regular users can't send emails
    
    
    def test_admin_can_access_customer_list(self):
        """Test that an admin user can access the customer list."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.customer_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_non_admin_cannot_access_customer_list(self):
        """Test that a non-admin user cannot access the customer list."""
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.get(self.customer_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class CartItemViewSetTest(APITestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.client = APIClient()

        # Create a user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)

        # Create a cart for the user
        self.cart = Cart.objects.create()

        # Create a category
        self.category = Category.objects.create(name="Office Supplies")
        
        # Create a product 
        self.product = Product.objects.create(
            name="Test Product",
            price=50.0,
            stock=10,
            category=self.category  
        )


        # Create a cart item
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)

        # Set URLs for tests
        self.cart_items_url = reverse("cart-items-list", kwargs={"cart_pk": str(self.cart.pk)})
        self.cart_item_detail_url = reverse("cart-items-detail", kwargs={"cart_pk": str(self.cart.pk), "pk": self.cart_item.pk})


    def test_get_cart_items_authenticated(self):
        """Test that an authenticated user can retrieve cart items."""
        response = self.client.get(self.cart_items_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Ensure one item exists in the cart
        self.assertEqual(response.data[0]["product"]["id"], self.product.id)


    def test_add_cart_item_authenticated(self):
        """Test that an authenticated user can add an item to the cart."""
        new_product = Product.objects.create(
            name="Test Product",
            price=50.0,
            stock=10,
            category=self.category  
        )

        payload = {
            "product": new_product.id,
            "quantity": 2
        }

        response = self.client.post(self.cart_items_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 2)


    def test_update_cart_item_authenticated(self):
        """Test that an authenticated user can update the quantity of a cart item."""
        payload = {
            "quantity": 3
        }

        response = self.client.patch(self.cart_item_detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 3)

    def test_delete_cart_item_authenticated(self):
        """Test that an authenticated user can remove an item from their cart."""
        response = self.client.delete(self.cart_item_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(pk=self.cart_item.pk).exists())


    def test_unauthenticated_user_cannot_access_cart(self):
        """Test that an unauthenticated user cannot access cart items."""
        self.client.logout()
        response = self.client.get(self.cart_items_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class CartViewSetTest(APITestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.client = APIClient()

        # Create a user and authenticate
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.force_authenticate(user=self.user)

        # Create a cart for the user
        self.cart = Cart.objects.create()

        # Set URLs for tests
        self.cart_list_url = reverse("cart-list")  # Ensure correct router registration
        self.cart_detail_url = reverse("cart-detail", kwargs={"pk": self.cart.pk})


    def test_create_cart_authenticated(self):
        """Test that an authenticated user can create a cart."""
        response = self.client.post(self.cart_list_url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cart.objects.filter(id=response.data["id"]).exists())


    def test_retrieve_cart_authenticated(self):
        """Test that an authenticated user can retrieve their cart."""
        response = self.client.get(self.cart_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(self.cart.pk))  # Cart ID is usually a UUID


    def test_delete_cart_authenticated(self):
        """Test that an authenticated user can delete their cart."""
        response = self.client.delete(self.cart_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cart.objects.filter(pk=self.cart.pk).exists())


    def test_unauthenticated_user_cannot_access_cart(self):
        """Test that an unauthenticated user cannot access cart details."""
        self.client.logout()  # Ensure user is logged out
        response = self.client.get(self.cart_detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class OrderViewSetTest(APITestCase):

    def setUp(self):
        """Set up test data before each test runs."""
        self.client = APIClient()

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com", 
            password="adminpass"
        )

        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",  
            password="password123"
        )

        # Create a customer linked to the regular user
        self.customer, created = Customer.objects.get_or_create(
            user=self.user
        )
        # Create a category
        self.category = Category.objects.create(name="Office Supplies")
        
        # Create a product
        self.product = Product.objects.create(
            name="Test Product",
            price=50.0,
            stock=10,
            category=self.category  
        )

        # Create an order for the regular user
        self.order = Order.objects.create(customer=self.customer)

        # Create an order item linked to the order
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

        # Define URLs
        self.order_list_url = reverse("order-list")
        self.order_detail_url = reverse("order-detail", kwargs={"pk": self.order.pk})

    def test_create_order_authenticated(self):
        """Test that an authenticated user can create an order."""
        self.client.force_authenticate(user=self.user)

        # Create a cart for the user
        cart = Cart.objects.create()

        # Add an item to the cart to satisfy the validation check
        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=1)

        payload = {
            "cart_id": str(cart.id) 
        }

        response = self.client.post(self.order_list_url, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Order.objects.filter(id=response.data["id"]).exists())


    def test_get_orders_authenticated_user(self):
        """Test that an authenticated user can retrieve only their orders."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.order_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Regular user sees only their orders

    def test_get_orders_admin(self):
        """Test that an admin user can retrieve all orders."""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(self.order_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  # Admin can see all orders


    def test_update_order_admin_only(self):
        """Test that only an admin can update an order."""
        self.client.force_authenticate(user=self.user)

        payload = {"status": "p"}
        response = self.client.patch(self.order_detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular user cannot update orders

        # Now authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.order_detail_url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_order_admin_only(self):
        """Test that only an admin can delete an order."""
        self.client.force_authenticate(user=self.user)

        # Delete all order items before deleting the order
        OrderItem.objects.filter(order=self.order).delete() 

        response = self.client.delete(self.order_detail_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular user cannot delete orders

        # Now authenticate as admin
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.order_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.pk).exists())

    def test_unauthenticated_user_cannot_access_orders(self):
        """Test that an unauthenticated user cannot access orders."""
        self.client.logout()
        response = self.client.get(self.order_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
