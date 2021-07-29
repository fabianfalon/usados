"""
Usados users tests tests_models
"""
from __future__ import unicode_literals

from django.test import TestCase

from usados.users.models import Profile, User

from ..models import Category, Publications


# Create your tests here.
class PublicationModelTest(TestCase):
    """ User model tests"""

    def setUp(self):
        self.category = Category.objects.create(name='autos usados')
        self.user = User.objects.create_user(
            username='jonsnow', email='iknow@nothing.com', password='youknownothingjonsnow',
            first_name='jon', last_name="snow",
        )
        self.profile = Profile.objects.create(
            id=244883570, user=self.user,
            birthdate="1991-06-17"
        )
        self.publication = Publications.objects.create(
            profile=self.profile,
            title='publicacion de test',
            model='2018',
            branch='Peugeot 208',
            price=500000.60,
            kilometers='60000',
            city='La Rioja',
            category=self.category
        )

    def test_category__str__(self):
        self.assertEqual(str(self.category), 'Category: autos usados')

    def test_category_is_active(self):
        self.assertTrue(self.category.is_active)

    def test_publication__str__(self):
        self.assertEqual(
            str(self.publication), '#publicacion de test - Peugeot 208 2018'
        )

    def test_publication_pictures(self):
        pictures = self.publication.get_pictures()
        self.assertEqual(pictures.count(), 0)
