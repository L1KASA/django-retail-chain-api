from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.v1.inventory.views import InventoryViewSet

router = DefaultRouter()
router.register(r'items', InventoryViewSet, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]
