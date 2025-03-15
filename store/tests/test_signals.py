from django.test import TestCase
from django.contrib.auth import get_user_model

from store.models import Customer



class TestCreateCustomerSignal(TestCase):


    def test_customer_profile_created_when_user_is_created(self):
        """✅ Test that a Customer profile is created when a new User is created."""
        User = get_user_model()
        
        # ✅ Create a new user
        user = User.objects.create_user(username="testuser", password="testpass")

        # ✅ Ensure that a Customer instance is automatically created
        customer_exists = Customer.objects.filter(user=user).exists()
        self.assertTrue(customer_exists)


    def test_customer_profile_not_created_for_existing_user(self):
        """✅ Test that the signal does not trigger for existing users."""
        User = get_user_model()

        # ✅ Create a new user
        user = User.objects.create_user(username="testuser2", password="testpass")

        # ✅ Get the customer count after user creation
        initial_customer_count = Customer.objects.count()

        # ✅ Save the user again (should NOT create a new customer)
        user.save()

        # ✅ Ensure customer count remains unchanged
        self.assertEqual(Customer.objects.count(), initial_customer_count)
        