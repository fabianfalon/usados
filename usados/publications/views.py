"""
Usados publications api views
"""

import logging

# Django rest framework
from rest_framework import status, viewsets
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

# Filters
from django_filters.rest_framework import DjangoFilterBackend

# Models
from .models import Publication
# Serializers
from .serializers import PublicationCreateSerializer, PublicationsModelSerializer

logger = logging.getLogger(__name__)


class PublicationsViewSet(viewsets.ModelViewSet):
    """
    PublicationsViewSet
    """
    queryset = Publication.objects.all()
    serializer_class = PublicationsModelSerializer

    # filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('title', 'model')
    ordering_filters = ('price', 'model')
    filterset_fields = ('is_active', 'model')

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['list']:
            permissions = [AllowAny, ]
        else:
            permissions = [IsAuthenticated, ]
        return [p() for p in permissions]

    # def get_queryset(self):
    #     """Filter publications by profile"""
    #     return Publications.objects.filter(profile=self.request.user.profile)

    def destroy(self, request, pk=None):
        raise MethodNotAllowed('DELETE')

    def create(self, request, *args, **kwargs):
        """publication create."""
        serializer = PublicationCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        publication = serializer.save()

        data = self.get_serializer(publication).data
        return Response(
            data, status=status.HTTP_201_CREATED
        )
