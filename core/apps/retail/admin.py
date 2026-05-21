from django.contrib import admin
from core.apps.retail.models import Employee, RetailPoint
from core.apps.retail.use_cases.clear_revenue import ClearRevenueUseCase


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
        from core.project.containers import get_container
        
        container = get_container()
        use_case = container.resolve(ClearRevenueUseCase)
        result = use_case.execute(list(queryset.values_list('id', flat=True)))
        self.message_user(request, result['status'])

    actions = ['clear_revenue']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone', 'email', 'retail_point', 'api_key')
    raw_id_fields = ('user', 'retail_point')
    readonly_fields = ('api_key',)
