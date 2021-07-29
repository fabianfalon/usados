"""Users URLs."""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
# router.register(
#     r'users/<int:id>/publications', UserPublicationViewSet, basename='user_publications'
# )

urlpatterns = [
    path('', include(router.urls))
]
