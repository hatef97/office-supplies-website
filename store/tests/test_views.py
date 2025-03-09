from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from store.models import Product, Category, Discount
from store.serializers import ProductSerializer




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
        # Create a category and discounts and product 
        self.category = Category.objects.create(name="Stationery")
        
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

    def test_admin_can_delete_product(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


    def test_regular_user_cannot_delete_product(self):
        self.client.login(username='regular', password='regularpass123')
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_unauthenticated_user_cannot_delete_product(self):
        response = self.client.delete(self.product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
