from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from store.models import Product, Category
from store.serializers import ProductSerializer




User = get_user_model()



class ProductViewSetTest(APITestCase):

    def setUp(self):
        # Create admin and regular user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
        )

        # Create a category and product
        self.category = Category.objects.create(name="Stationery")
        self.product = Product.objects.create(
            name="Notebook",
            price=5.99,
            stock=100,
            category=self.category
        )

        self.product_url = reverse('product-detail', args=[self.product.id])


    def test_admin_can_delete_product(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())


    def test_regular_user_cannot_delete_product(self):
        self.client.login(username='regular', password='regularpass123')
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_unauthenticated_user_cannot_delete_product(self):
        response = self.client.delete(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
