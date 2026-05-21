from celery import shared_task
from core.apps.retail.models import RetailPoint
from core.project.containers import get_container
from core.apps.retail.services.revenue import RevenueService
from core.apps.inventory.services.stock import StockService


@shared_task
def clear_daily_revenue_task(point_ids: list[int]) -> dict:
    """Асинхронное обнуление выручки"""
    container = get_container()
    service = container.resolve(RevenueService)
    
    points = RetailPoint.objects.filter(
        id__in=point_ids,
        point_type=RetailPoint.PointType.DEALER,
    )
    count = service.clear_daily_revenue(points)
    return {'status': 'ok', 'cleared': count}


@shared_task
def replenish_zero_stock_task() -> dict:
    """Пополнить нулевые остатки"""
    container = get_container()
    service = container.resolve(StockService)
    count = service.replenish_zero_stock()
    return {'status': 'ok', 'replenished': count}


@shared_task
def clear_all_revenue_task() -> dict:
    """Обнулить выручку у всех дилеров"""
    container = get_container()
    service = container.resolve(RevenueService)
    
    points = RetailPoint.objects.filter(point_type=RetailPoint.PointType.DEALER)
    count = service.clear_daily_revenue(points)
    return {'status': 'ok', 'cleared': count}
