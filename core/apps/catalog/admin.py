from django.contrib import admin

from core.apps.catalog.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'price', 'release_date')
    list_display_links = ('brand', 'model')
    search_fields = ('brand', 'model')
    list_filter = ('brand', 'release_date')
    ordering = ('brand', 'model')
    