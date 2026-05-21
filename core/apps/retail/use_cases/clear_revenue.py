from typing import List
from core.apps.retail.models import RetailPoint
from core.apps.retail.services.revenue import RevenueService


class ClearRevenueUseCase:
    def __init__(self, revenue_service: RevenueService):
        self.revenue_service = revenue_service

    def execute(self, point_ids: List[int], async_threshold: int = 5) -> dict:
        if len(point_ids) > async_threshold:
            from tasks.daily import clear_daily_revenue_task
            clear_daily_revenue_task.delay(point_ids)
            return {'status': f'Запущена асинхронная очистка для {len(point_ids)} точек'}

        points = RetailPoint.objects.filter(id__in=point_ids)
        count = self.revenue_service.clear_revenue(points)
        return {'status': f'Очищено точек: {count}'}
