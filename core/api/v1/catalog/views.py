from rest_framework import viewsets

from core.api.v1.catalog.serializers import ProductSerializer
from core.apps.catalog.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
