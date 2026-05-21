from decimal import Decimal

from django.db.models import QuerySet, Avg

from core.apps.retail.models import RetailPoint


class RetailPointSelector:
    @staticmethod
    def filter_by_city(city: str) -> QuerySet[RetailPoint]:
        return RetailPoint.objects.filter(city__icontains=city)

    @staticmethod
    def points_with_product(product_id: int) -> QuerySet[RetailPoint]:
        return RetailPoint.objects.filter(
            point_type=RetailPoint.PointType.DEALER,
            inventory_items__product_id=product_id,
            inventory_items__quantity__gt=0,
        ).distinct()

    @staticmethod
    def dealers_above_average() -> QuerySet[RetailPoint]:
        avg = (
            RetailPoint.objects
            .filter(point_type=RetailPoint.PointType.DEALER)
            .aggregate(avg=Avg('daily_revenue'))['avg']
        ) or Decimal('0.00')
        return RetailPoint.objects.filter(
            point_type=RetailPoint.PointType.DEALER,
            daily_revenue__gt=avg,
        )
