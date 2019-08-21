from django.test import TestCase

from .models import Enterprise

# Create your tests here.
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase

from .views import index, deletemodel

class AuthTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_auth_index_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('index')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        # Use this syntax for class-based views.
        
        self.assertEqual(response.status_code, 200)

class DeleteModelTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_delete_model_view(self):
        # Create an instance of a GET request.
        request = self.factory.get('deletemodel/42')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        #request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = deletemodel(request)
        # Use this syntax for class-based views.
        
        self.assertEqual(response.status_code, 200)
        