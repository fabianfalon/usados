# Django REST Framework
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

# Serializers
from usados.users.serializers import ProfileModelSerializer

# Models
from .models import Category, Publication

# Utils
from usados.utils import DynamicFieldsModelSerializer


class PublicationsModelSerializer(DynamicFieldsModelSerializer):
    """PublicationsModelSerializer"""
    profile = ProfileModelSerializer(read_only=True)
    pictures = serializers.StringRelatedField(many=True)

    class Meta:
        model = Publication
        fields = (
            'profile',
            'id',
            'title',
            'type_of_publication',
            'price',
            'category',
            'is_active',
            'is_premium',
            'pictures'
        )


class PublicationCreateSerializer(serializers.Serializer):
    """create publication serializer."""
    title = serializers.CharField()
    model = serializers.CharField()
    type_of_publication = serializers.CharField()
    price = serializers.CharField()
    category = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, data):
        """Create new Publication."""
        user = data['user']
        category = get_object_or_404(Category, id=data['category'])
        data.pop('user')
        data.pop('category')
        if user.profile.publications_numbers < 5:
            publication = Publication.objects.create(
                profile=user.profile,
                category=category,
                **data
            )
            user.profile.publications_numbers += 1
            user.profile.save()
            return publication
        else:
            raise serializers.ValidationError(
                'You dont have more free publications.'
            )
