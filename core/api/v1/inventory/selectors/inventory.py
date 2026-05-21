from django.db.models import QuerySet

from core.apps.inventory.models import Inventory


class InventorySelector:
    @staticmethod
    def get_all() -> QuerySet[Inventory]:
        return Inventory.objects.all()

    @staticmethod
    def filter_by_product(qs: QuerySet[Inventory], product_id: int) -> QuerySet[Inventory]:
        return qs.filter(product_id=product_id)

    @staticmethod
    def filter_by_retail_point(qs: QuerySet[Inventory], retail_point_id: int) -> QuerySet[Inventory]:
        return qs.filter(retail_point_id=retail_point_id)

    @staticmethod
    def filter_in_stock(qs: QuerySet[Inventory]) -> QuerySet[Inventory]:
        return qs.filter(quantity__gt=0)

    @staticmethod
    def filter_out_of_stock(qs: QuerySet[Inventory]) -> QuerySet[Inventory]:
        return qs.filter(quantity=0)
