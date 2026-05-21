from core.api.permissions import IsActiveEmployee, IsOwnerEmployee


class ApiKeyPermissionMixin:
    def get_permissions(self) -> list:
        if self.request.headers.get('X-API-Key') or self.request.query_params.get('api_key'):
            return [IsOwnerEmployee()]
        return [IsActiveEmployee()]
