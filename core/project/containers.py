from functools import lru_cache

import punq

from core.apps.retail.services.revenue import RevenueService
from core.apps.retail.use_cases.clear_revenue import ClearRevenueUseCase


@lru_cache(1)
def get_container() -> punq.Container:
    container = punq.Container()

    # Services
    container.register(RevenueService)

    # Use cases
    container.register(ClearRevenueUseCase)

    return container
