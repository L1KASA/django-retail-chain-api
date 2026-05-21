from rest_framework import serializers

from core.apps.inventory.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.__str__', read_only=True)
    retail_point_name = serializers.CharField(source='retail_point.name', read_only=True)

    class Meta:
        model = Inventory
        fields = (
            'id', 'product', 'product_name', 'retail_point', 'retail_point_name',
            'quantity', 'created_at', 'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
