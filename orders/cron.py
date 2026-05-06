from orders.interactors.order.release_scheduled_orders_interactor import (
    ReleaseScheduledOrdersInteractor,
)
from orders.storages.order_storage import OrderStorage


def release_scheduled_orders():
    interactor = ReleaseScheduledOrdersInteractor(
        order_storage=OrderStorage(),
    )
    interactor.release_scheduled_orders()
