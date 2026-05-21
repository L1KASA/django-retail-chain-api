from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.api.v1.retail.views import RetailPointViewSet

router = DefaultRouter()
router.register(r'points', RetailPointViewSet, basename='retail-point')

urlpatterns = [
    path('', include(router.urls)),
]
