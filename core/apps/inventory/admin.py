from django.contrib import admin
from core.apps.inventory.models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'retail_point', 'quantity', 'created_at')
    list_display_links = ('product', 'retail_point')
    list_filter = (
        'retail_point', 
        'quantity',
    )
    search_fields = ('product__brand', 'product__model', 'retail_point__name')
    raw_id_fields = ('product',)
    