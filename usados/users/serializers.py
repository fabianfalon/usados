from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .models import Profile, User


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.profile.can_access():
            raise serializers.ValidationError('Account is not active')
        payload = jwt_payload_handler(user)
        self.context['user'] = user
        token = jwt_encode_handler(payload)
        self.context['token'] = token
        return data

    def create(self, data):
        """Generate or retrieve new token."""
        return self.context['user'], self.context['token']


class UserModelSerializerToProfile(serializers.ModelSerializer):
    """User model serializer."""
    class Meta:
        """Meta class."""

        model = User
        fields = (
            'email',
            'first_name',
            'last_name'
        )


class ProfileModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializerToProfile(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'address',
            'publications_numbers',
            'birthdate',
            'status',
            'picture'
        )


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""
    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'profile',
        )


class UserSignUpSerializer(serializers.Serializer):
    """User sign up serializer.
    Handle sign up data validation and user/profile creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)
    birthdate = serializers.CharField(min_length=2, max_length=30)

    address = serializers.CharField(min_length=2, max_length=255, required=False)
    user_type = serializers.IntegerField(required=False)
    dni = serializers.CharField(min_length=2, max_length=255, required=False)

    def validate_birthdate(self, data):
        if not data:
            raise serializers.ValidationError(
                'Birthdate is mandatory.'
            )
        return data

    def validate(self, data):
        """Verify passwords match."""
        password = data['password']
        password_confirmation = data['password_confirmation']
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(password)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')

        username = "{}{}".format(
            data['first_name'],
            data['last_name']
        )
        user = User.objects.create_user(
            email=data['email'],
            username=username,
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name']
        )
        data.pop('email')
        data.pop('first_name')
        data.pop('last_name')
        data.pop('password')

        Profile.objects.create(
            user=user,
            **data
        )
        return user
