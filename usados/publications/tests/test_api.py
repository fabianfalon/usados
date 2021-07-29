# Django REST Framework
from rest_framework import status
from rest_framework.test import APITestCase

from usados.users.models import Profile, User

from ..models import Category


class UserAPITestCase(APITestCase):
    """User API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create_user(
            username='jonsnow', email='iknow@nothing.com',
            password='youknownothingjonsnow',
            first_name='jons', last_name="now",
        )
        self.profile = Profile.objects.create(
            id=244883570, user=self.user,
            birthdate="1991-06-17"
        )
        self.category = Category.objects.create(
            name="categoria de prueba"
        )
        # URL
        self.url = '/api/v1/publications/'
        self.url_with_params = self.url + '?search=2005' 
        self.data = {
            'profile': self.profile,
            'title': 'Publicacion de prueba',
            'model': '2005',
            'branch': 'Peugeot 2008',
            'type_of_publication': 1,
            'price': 520555.33,
            'kilometers': '55000',
            'city': 'La Rioja',
            'category': self.category.id
        }

    def test_post_publications_with_anonymous_user(self):
        response = self.client.post(
            self.url, self.data, **{'wsgi.url_scheme': 'https'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_publications_success(self):
        """Verify create publications succeed."""
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, self.data, **{'wsgi.url_scheme': 'https'})
        self.assertTrue(response.data['is_active'])
        self.assertFalse(response.data['is_premium'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.profile.publications_numbers, 1)

    def test_get_publications_with_anonymous_user(self):
        response = self.client.get(self.url, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_publications_success(self):
        """Verify get publications succeed."""
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_publications_success(self):
        """Verify get publications succeed."""
        response = self.client.get(self.url_with_params, **{'wsgi.url_scheme': 'https'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def tearDown(self):
        self.client.logout()
