import random
from decimal import Decimal

from core.apps.inventory.models import Inventory


class StockService:
    @staticmethod
    def reduce_stock(item: Inventory, reduction: int) -> Decimal:
        item.quantity = max(0, item.quantity - reduction)
        item.save()
        return item.product.price * reduction

    @staticmethod
    def replenish_zero_stock():
        items = Inventory.objects.filter(quantity=0)
        count = 0
        for item in items:
            item.quantity = random.randint(5, 25)
            item.save()
            count += 1
        return count
