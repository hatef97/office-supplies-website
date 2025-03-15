from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from store.permissions import SendPrivateEmailToCustomerPermission
from store.views import CustomerViewSet 



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
