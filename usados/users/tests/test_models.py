"""
Usados users tests tests_models
"""
from __future__ import unicode_literals

from django.test import TestCase

from ..models import Profile, User


# Create your tests here.
class UserModelTest(TestCase):
    """ User model tests"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='jonsnow', email='iknow@nothing.com', password='youknownothingjonsnow',
            first_name='jon', last_name="snow",
        )
        self.profile = Profile.objects.create(
            id=244883570, user=self.user,
            birthdate="1991-06-17"
        )

    def test__str__(self):
        self.assertEqual(str(self.profile), 'jon snow')

    def test__publications_numbers(self):
        self.assertEqual(self.profile.publications_numbers, 0)
