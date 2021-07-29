"""
Usados tests serializers
"""
from __future__ import unicode_literals

from django.test import TestCase

from ..models import Profile, User
from ..serializers import ProfileModelSerializer, UserSignUpSerializer


# Create your tests here.
class SerializerTest(TestCase):
    """ Tests for SerializerTest creation """

    def setUp(self):
        self.user = User.objects.create_user(
            username='jonsnow', email='iknow@nothing.com', password='youknownothingjonsnow',
            first_name='jonsnow', last_name="starck",
        )
        self.profile = Profile.objects.create(
            id=244883570, user=self.user,
            birthdate="1991-06-17"
        )
        self.profile_serializer = ProfileModelSerializer(instance=self.profile)
        self.serializer_data = {
            "email": "test@gtest.com",
            "first_name": "test1",
            "last_name": "test1",
            "password": "probandopass1",
            "password_confirmation": "probandopass1",
            "birthdate": "2001-05-12"
        }

    def test_profile_serializer(self):
        self.profile_serializer.data['dni'] = '35541117'
        serializer = ProfileModelSerializer(data=self.profile_serializer)
        self.assertFalse(serializer.is_valid())

    def test_user_singup_serializer(self):
        serializer = UserSignUpSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())

    def test_user_singup_pass_error_serializer(self):
        self.serializer_data['password'] = 'test1'
        serializer = UserSignUpSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['password']))
