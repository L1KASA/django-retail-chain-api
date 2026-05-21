from django.contrib import admin
from core.apps.retail.models import Employee, RetailPoint


@admin.register(RetailPoint)
class RetailPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'point_type', 'country', 'city', 'street', 'house_number', 'daily_revenue')
    list_filter = (
        'country',
        'point_type',
    )
    search_fields = ('name', 'city', 'street')
    
    @admin.action(description='Очистить суточную выручку')
    def clear_revenue(self, request, queryset):
        # TODO: сделать очистку выручки. Метод из RevenueService
        pass

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone', 'email', 'retail_point', 'api_key')
    raw_id_fields = ('user', 'retail_point')
    readonly_fields = ('api_key',)