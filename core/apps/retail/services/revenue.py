from decimal import Decimal

from django.db.models import QuerySet, Avg

from core.apps.retail.models import RetailPoint
from core.apps.retail.exceptions import RevenueClearException


class RevenueService:
    """Бизнес-логика работы с выручкой."""

    @staticmethod
    def clear_revenue(points: QuerySet[RetailPoint]) -> int:
        """Обнуление выручки у точек"""
        if points.filter(point_type=RetailPoint.PointType.HEAD_OFFICE).exists():
            raise RevenueClearException()
        return points.update(daily_revenue=Decimal('0.00'))

    @staticmethod
    def get_average_revenue() -> Decimal:
        """Средняя выручка по дилерским центрам"""
        dealers = RetailPoint.objects.filter(point_type=RetailPoint.PointType.DEALER)
        result = dealers.aggregate(avg=Avg('daily_revenue'))['avg']
        return result or Decimal('0.00')
