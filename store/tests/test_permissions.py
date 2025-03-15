from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIRequestFactory
from rest_framework.permissions import SAFE_METHODS

from store.permissions import *
from store.views import CustomerViewSet, CategoryViewSet  



User = get_user_model()



class SendPrivateEmailToCustomerPermissionTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create a user without permissions
        self.user_without_permission = User.objects.create_user(
            username="no_permission_user",
            email="no_permission@example.com", 
            password="password123"
        )
        # Create a user with the required permission
        self.user_with_permission = User.objects.create_user(username="has_permission_user", password="password123")
        permission = Permission.objects.get(codename="send_private_email")
        self.user_with_permission.user_permissions.add(permission)

        # Set up a test view that uses this permission
        self.view = CustomerViewSet.as_view({'get': 'list'})  # Adjust according to your API


    def test_permission_granted(self):
        """✅ Test that a user with 'send_private_email' permission is granted access."""
        request = self.factory.get('/fake-url/')
        request.user = self.user_with_permission

        permission = SendPrivateEmailToCustomerPermission()
        self.assertTrue(permission.has_permission(request, self.view))


    def test_permission_denied_without_permission(self):
        """🚫 Test that a user without 'send_private_email' permission is denied access."""
        request = self.factory.get('/fake-url/')
        request.user = self.user_without_permission

        permission = SendPrivateEmailToCustomerPermission()
        self.assertFalse(permission.has_permission(request, self.view))


    def test_permission_denied_for_anonymous_user(self):
        """🚫 Test that an unauthenticated user is denied access."""
        request = self.factory.get('/fake-url/')
        request.user = None  # Simulate an anonymous user

        permission = SendPrivateEmailToCustomerPermission()
        self.assertFalse(permission.has_permission(request, self.view))



class IsAdminOrReadOnlyTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # ✅ Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass"
        )

        # ✅ Create a regular user
        self.regular_user = User.objects.create_user(
            username="regular_user",
            email="user@example.com",
            password="userpass"
        )

        # ✅ Set up a test view
        self.view = CategoryViewSet.as_view({'get': 'list'})


    def test_admin_has_full_access(self):
        """✅ Admins should be able to access all methods (GET, POST, PUT, DELETE)."""
        permission = IsAdminOrReadOnly()

        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            request = self.factory.generic(method, '/fake-url/')
            request.user = self.admin_user
            self.assertTrue(permission.has_permission(request, self.view))


    def test_regular_user_has_read_only_access(self):
        """✅ Regular users should be allowed only safe methods (GET) and denied others."""
        permission = IsAdminOrReadOnly()

        # ✅ GET should be allowed
        request = self.factory.get('/fake-url/')
        request.user = self.regular_user
        self.assertTrue(permission.has_permission(request, self.view))

        # ❌ POST, PUT, DELETE should be denied
        for method in ['POST', 'PUT', 'DELETE']:
            request = self.factory.generic(method, '/fake-url/')
            request.user = self.regular_user
            self.assertFalse(permission.has_permission(request, self.view))


    def test_anonymous_user_has_read_only_access(self):
        """✅ Anonymous users should be allowed only safe methods (GET) and denied others."""
        permission = IsAdminOrReadOnly()

        # ✅ GET should be allowed
        request = self.factory.get('/fake-url/')
        request.user = None  # Simulate an anonymous user
        self.assertTrue(permission.has_permission(request, self.view))

        # ❌ POST, PUT, DELETE should be denied
        for method in ['POST', 'PUT', 'DELETE']:
            request = self.factory.generic(method, '/fake-url/')
            request.user = None
            self.assertFalse(permission.has_permission(request, self.view))
