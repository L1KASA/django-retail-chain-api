from django.urls import path, include

urlpatterns = [
    path('retail/', include('core.api.v1.retail.urls')),
    path('catalog/', include('core.api.v1.catalog.urls')),
    path('inventory/', include('core.api.v1.inventory.urls')),
]
