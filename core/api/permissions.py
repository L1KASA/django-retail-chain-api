from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from core.apps.retail.models import Employee


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.user.is_authenticated
            and request.user.is_active
            and hasattr(request.user, 'employee')
        )


class IsOwnerEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('X-API-Key') or request.query_params.get('api_key')
        if not api_key:
            return False

        try:
            employee = Employee.objects.get(api_key=api_key)
            request.employee = employee
            return True
        except Employee.DoesNotExist:
            return False
        
    def has_object_permission(self, request, view, obj) -> bool:
        if hasattr(obj, 'retail_point'):
            return obj.retail_point == request.employee.retail_point
        if hasattr(obj, 'retail_point_id'):
            return obj.retail_point_id == request.employee.retail_point_id
        return False
