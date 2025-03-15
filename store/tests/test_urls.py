from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import *


class URLPatternsTest(SimpleTestCase):


    def test_category_list_url(self):
        """Test that the category list URL is correctly mapped."""
        url = reverse('category-list')
        self.assertEqual(resolve(url).func.cls, CategoryViewSet)


    def test_product_list_url(self):
        """Test that the product list URL is correctly mapped."""
        url = reverse('product-list')
        self.assertEqual(resolve(url).func.cls, ProductViewSet)


    def test_customer_list_url(self):
        """Test that the customer list URL is correctly mapped."""
        url = reverse('customer-list')
        self.assertEqual(resolve(url).func.cls, CustomerViewSet)


    def test_cart_list_url(self):
        """Test that the cart list URL is correctly mapped."""
        url = reverse('cart-list')
        self.assertEqual(resolve(url).func.cls, CartViewSet)


    def test_order_list_url(self):
        """Test that the order list URL is correctly mapped."""
        url = reverse('order-list')
        self.assertEqual(resolve(url).func.cls, OrderViewSet)


    def test_category_products_nested_url(self):
        """Test that the nested category products URL is correctly mapped."""
        url = reverse('category-products-list', kwargs={'category_pk': 1}) 
        self.assertEqual(resolve(url).func.cls, ProductViewSet)


    def test_cart_items_nested_url(self):
        """Test that the nested cart items URL is correctly mapped."""
        url = reverse('cart-items-list', kwargs={'cart_pk': 1})
        self.assertEqual(resolve(url).func.cls, CartItemViewSet)


    def test_product_comments_nested_url(self):
        """Test that the nested product comments URL is correctly mapped."""
        url = reverse('product-comments-list', kwargs={'product_pk': 1})
        self.assertEqual(resolve(url).func.cls, CommentViewSet)
