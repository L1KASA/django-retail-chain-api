from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.api.mixins import ApiKeyPermissionMixin
from core.api.v1.retail.serializers import RetailPointSerializer
from core.apps.retail.models import RetailPoint
from core.apps.retail.selectors.retail_point import RetailPointSelector
from core.apps.retail.exceptions import HeadOfficeDeleteException
from core.apps.retail.use_cases.clear_revenue import ClearRevenueUseCase
from core.project.containers import get_container


class RetailPointViewSet(ApiKeyPermissionMixin, viewsets.ModelViewSet):
    queryset = RetailPoint.objects.all()
    serializer_class = RetailPointSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        
        if hasattr(self.request, 'employee'):
            return qs.filter(id=self.request.employee.retail_point_id)

        city = self.request.GET.get('city')
        if city:
            qs = RetailPointSelector.filter_by_city(city)

        product_id = self.request.GET.get('product_id')
        if product_id:
            qs = RetailPointSelector.points_with_product(product_id)

        return qs

    @action(detail=False, methods=['get'])
    def get_high_daily_revenue(self, request: Request) -> Response:
        """Получить дилеров с выручкой выше средней"""
        dealers = RetailPointSelector.dealers_above_average()
        serializer = self.get_serializer(dealers, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def clear_revenue(self, request: Request) -> Response:
        """Обнулить выручку (daily_revenue) у указанных точек"""
        container = get_container()
        use_case = container.resolve(ClearRevenueUseCase)
        result = use_case.execute(request.data.get('point_ids', []))
        return Response(result)

    def perform_destroy(self, instance: RetailPoint) -> None:
        """Удалить торговую точку"""
        if instance.is_head_office:
            raise HeadOfficeDeleteException()
        instance.delete()

    def perform_update(self, serializer: RetailPointSerializer) -> None:
        """Обновить торговую точку"""
        serializer.save()