from functools import lru_cache

import punq

from core.apps.retail.services.revenue import RevenueService
from core.apps.retail.use_cases.clear_revenue import ClearRevenueUseCase
from core.apps.inventory.services.stock import StockService
from core.apps.inventory.use_cases.reduce_random_stock import ReduceRandomStockUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(RevenueService)
    container.register(StockService)

    # Use cases
    container.register(ClearRevenueUseCase)
    container.register(ReduceRandomStockUseCase)

    return container
