from dataclasses import dataclass
from typing import List

from core.apps.retail.models import RetailPoint
from core.apps.retail.services.revenue import RevenueService


@dataclass
class ClearRevenueUseCase:
    revenue_service: RevenueService

    def execute(self, point_ids: List[int], async_threshold: int = 5) -> dict:
        if len(point_ids) > async_threshold:
            # TODO: добавить celery
            return {'status': f'Запущена асинхронная очистка для {len(point_ids)} точек'}

        points = RetailPoint.objects.filter(id__in=point_ids)
        count = self.revenue_service.clear_revenue(points)
        return {'status': f'Очищено точек: {count}'}
