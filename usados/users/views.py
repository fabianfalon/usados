"""
usados users api views
"""

import logging

# Django REST Framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
# Permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from usados.publications.serializers import PublicationsModelSerializer

from .models import User
from .serializers import ProfileModelSerializer, UserLoginSerializer, UserModelSerializer, UserSignUpSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsAuthenticated, ]
        return [p() for p in permissions]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User sign in."""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'])
    def profile(self, request, *args, **kwargs):
        """Update profile data."""
        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            'user': response.data
        }
        response.data = data
        return response

    @action(detail=True, methods=['get'])
    def publications(self, request, *args, **kwargs):
        """Return user publications."""
        profile = request.user.profile
        publications = profile.get_publications()
        if publications:
            data = PublicationsModelSerializer(publications, many=True).data
            return Response(data)
        else:
            return Response(
                {"message": "the user has not publications"},
                status=status.HTTP_200_OK,
            )
