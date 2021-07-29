# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase


class UserAPITestCase(APITestCase):
    """User API test case."""

    def setUp(self):
        """Test case setup."""
        # URL
        self.url = '/api/v1/users/signup/'
        self.data = {
            "email": "test@test.com",
            "first_name": "test1",
            "last_name": "test2",
            "password": "testeandopasss",
            "password_confirmation": "testeandopasss",
            "birthdate": "2001-05-12"
        }
    # singup tests

    def test_singup_success(self):
        """Verify singup succeed."""
        request = self.client.post(self.url, self.data, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_singup_without_email(self):
        """Verify singup without email."""
        self.data.pop('email')
        request = self.client.post(self.url, self.data, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_singup_with_differents_pss(self):
        """Verify singup with diffetents pass."""
        self.data['password_confirmation'] = "otra pass"
        request = self.client.post(self.url, self.data, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
