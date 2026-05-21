from rest_framework import viewsets

from core.api.mixins import ApiKeyPermissionMixin
from core.api.v1.inventory.selectors.inventory import InventorySelector
from core.api.v1.inventory.serializers import InventorySerializer
from core.apps.inventory.models import Inventory


class InventoryViewSet(ApiKeyPermissionMixin, viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

    def get_queryset(self):
        qs = InventorySelector.get_all()

        if hasattr(self.request, 'employee'):
            return qs.filter(retail_point=self.request.employee.retail_point)

        product_id = self.request.GET.get('product_id')
        if product_id:
            qs = InventorySelector.filter_by_product(qs, int(product_id))

        retail_point_id = self.request.GET.get('retail_point_id')
        if retail_point_id:
            qs = InventorySelector.filter_by_retail_point(qs, int(retail_point_id))

        in_stock = self.request.GET.get('in_stock')
        if in_stock == '1':
            qs = InventorySelector.filter_in_stock(qs)
        elif in_stock == '0':
            qs = InventorySelector.filter_out_of_stock(qs)

        return qs
