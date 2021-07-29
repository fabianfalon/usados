"""Publications URLs."""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import PublicationsViewSet

router = DefaultRouter()
router.register(r'publications', PublicationsViewSet, basename='publications')

urlpatterns = [
    path('', include(router.urls))
]
