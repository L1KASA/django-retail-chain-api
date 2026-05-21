from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.user.is_authenticated
            and request.user.is_active
            and hasattr(request.user, 'employee')
        )
