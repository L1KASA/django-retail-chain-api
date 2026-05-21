import random
from decimal import Decimal

from core.apps.inventory.services.stock import StockService
from core.apps.retail.models import RetailPoint


class ReduceRandomStockUseCase:
    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def execute(self):
        dealers = RetailPoint.objects.filter(
            point_type=RetailPoint.PointType.DEALER,
            inventory_items__quantity__gt=0,
        ).distinct()

        if not dealers:
            return {'status': 'ok', 'message': 'Нет дилеров с товарами'}

        dealer = random.choice(list(dealers))
        items = list(dealer.inventory_items.filter(quantity__gt=0))
        selected = random.sample(items, min(3, len(items)))
        total_revenue = Decimal('0.00')
        emptied = []

        for item in selected:
            reduction = random.randint(1, 10)
            revenue = self.stock_service.reduce_stock(item, reduction)
            total_revenue += revenue
            if item.quantity == 0:
                emptied.append(item)

        dealer.daily_revenue += total_revenue
        dealer.save()

        for item in emptied:
            from tasks.hourly import send_low_stock_email_task
            send_low_stock_email_task.delay(dealer.id, item.product.id)

        return {
            'status': 'ok',
            'dealer': dealer.name,
            'reduction': total_revenue,
            'emptied': len(emptied),
        }
