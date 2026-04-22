import pytest

from order.constants.enums import OrderStatus
from order.interactors.dtos import CreateOrderItemDTO
from order.models import OrderItem
from order.storages.order_storage import OrderStorage
from order.tests.factories.dto_factories import CreateOrderDTOFactory
from order.tests.factories.storage_factories import OrderFactory, PromoCodeFactory


@pytest.mark.django_db
class TestOrderStorage:
    def setup_method(self):
        self.storage = OrderStorage()

    def test_get_order_successfully(self):
        order = OrderFactory(
            id="order-1",
            customer_id="customer-1",
            restaurant_id="restaurant-1",
            items_total=400.0,
            delivery_fee=30.0,
            tax_fee=20.0,
            final_amount=450.0,
            address_id="1",
        )

        result = self.storage.get_order(order_id="order-1")

        assert result is not None
        assert result.order_id == "order-1"
        assert result.customer_id == "customer-1"
        assert result.restaurant_id == "restaurant-1"
        assert result.promo_code_id == order.promo_code.id
        assert result.items_total == 400.0
        assert result.delivery_fee == 30.0
        assert result.tax_fee == 20.0
        assert result.final_amount == 450.0
        assert result.address_id == "1"

    def test_get_order_returns_none_when_not_found(self):
        result = self.storage.get_order(order_id="invalid-order")

        assert result is None

    def test_create_order_successfully_with_promo_code(self):
        promo_code = PromoCodeFactory()
        create_order_dto = CreateOrderDTOFactory(
            customer_id="customer-1",
            restaurant_id="restaurant-1",
            promo_code_id=promo_code.id,
            items_total=400.0,
            delivery_fee=30.0,
            tax_fee=17.5,
            final_amount=397.5,
            address_id=1,
        )

        result = self.storage.create_order(create_order_dto=create_order_dto)

        assert result.order_id is not None
        assert result.customer_id == "customer-1"
        assert result.restaurant_id == "restaurant-1"
        assert result.promo_code_id == promo_code.id
        assert result.status == OrderStatus.PLACED
        assert result.items_total == 400.0
        assert result.delivery_fee == 30.0
        assert result.tax_fee == 17.5
        assert result.final_amount == 397.5

    def test_create_order_successfully_without_promo_code(self):
        create_order_dto = CreateOrderDTOFactory(promo_code_id=None)

        result = self.storage.create_order(create_order_dto=create_order_dto)

        assert result.order_id is not None
        assert result.promo_code_id is None

    def test_get_promo_code_usage_excludes_cancelled_orders(self):
        promo_code = PromoCodeFactory()
        OrderFactory(promo_code=promo_code, status=OrderStatus.PLACED.value)
        OrderFactory(promo_code=promo_code, status=OrderStatus.CONFIRMED.value)
        OrderFactory(promo_code=promo_code, status=OrderStatus.CANCELLED.value)

        result = self.storage.get_promo_code_usage(promo_code_id=promo_code.id)

        assert result == 2

    def test_create_order_items_successfully(self):
        order = OrderFactory(id="order-1")
        order_item_dtos = [
            CreateOrderItemDTO(
                order_id=order.id,
                item_id="item-1",
                quantity=2,
                item_price=200.0,
            ),
            CreateOrderItemDTO(
                order_id=order.id,
                item_id="item-2",
                quantity=1,
                item_price=150.0,
            ),
        ]

        self.storage.create_order_items(order_item_dtos=order_item_dtos)

        order_items = OrderItem.objects.filter(order_id=order.id).order_by("item_id")
        assert order_items.count() == 2

    def test_update_order_status_successfully(self):
        OrderFactory(id="order-1", status=OrderStatus.PLACED.value)

        result = self.storage.update_order_status(
            order_id="order-1",
            status=OrderStatus.CONFIRMED,
        )

        assert result is not None
        assert result.order_id == "order-1"
        assert result.status == OrderStatus.CONFIRMED

    def test_update_order_status_returns_none_when_order_not_found(self):
        result = self.storage.update_order_status(
            order_id="invalid-order",
            status=OrderStatus.CONFIRMED,
        )

        assert result is None
