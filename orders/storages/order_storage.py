from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import List

from django.db.models import Count, Q, Avg, Sum, ExpressionWrapper, F, DecimalField
from django.db.models.functions import ExtractHour

from orders.app_service.dtos import RestaurantOrdersSummaryDTO, OrdersByStatusDTO
from orders.constants.enums import OrderStatus
from orders.interactors.dtos import (
    CreateOrderDTO,
    CreateOrderItemDTO,
    OrderDTO,
    OrderItemSummaryDTO,
    TopSellingItemDTO,
    PeakHourDTO,
    OrderItemDTO,
)
from orders.interactors.storage_interface.order_storage_interface import (
    OrderStorageInterface,
)
from orders.models import Order, OrderItem


class OrderStorage(OrderStorageInterface):

    # TODO: Private methods should be preferably at the last.
    @staticmethod
    def _convert_to_order_dto(order_obj: Order) -> OrderDTO:
        return OrderDTO(
            order_id=str(order_obj.id),
            customer_id=str(order_obj.customer_id),
            restaurant_id=str(order_obj.restaurant_id),
            promo_code_id=order_obj.promo_code_id if order_obj.promo_code_id else None, # TODO: Why this if condition? 
            status=OrderStatus(order_obj.status),
            items_total=Decimal(order_obj.items_total), # TODO: I guess we will get decimal object why are we type castinig it again.
            delivery_fee=Decimal(order_obj.delivery_fee),
            tax_fee=Decimal(order_obj.tax_fee),
            final_amount=Decimal(order_obj.final_amount),
            address_id=order_obj.address_id,
            placed_at=order_obj.created_at,
        )

    def get_order(self, order_id: str) -> OrderDTO | None:  # TODO: This should be option instead of | None
        order_obj = Order.objects.filter(id=order_id).first()

        if order_obj is None:
            return None

        return self._convert_to_order_dto(order_obj=order_obj)

    def get_order_items(self, order_id: str) -> List[OrderItemSummaryDTO]:
        order_items = OrderItem.objects.filter(order_id=order_id).order_by(
            "created_at", "id"
        )

        return [
            OrderItemSummaryDTO(
                item_id=order_item.item_id,
                quantity=order_item.quantity,
                item_price=Decimal(order_item.item_price),
                subtotal=Decimal(order_item.item_price) * order_item.quantity,
            )
            for order_item in order_items
        ]

    def get_promo_code_usage(self, promo_code_id: int) -> int:
        # TODO: Why is promocode usage method in this class?s
        # TODO: also ignores valid_from/valid_until — counts lifetime usage even if the promo got reissued.
        return (
            Order.objects.filter(
                promo_code_id=promo_code_id,
            )
            .exclude(status=OrderStatus.CANCELLED.value)
            .count()
        )

    def create_order(self, create_order_dto: CreateOrderDTO) -> OrderDTO:
        order_obj = Order.objects.create(
            customer_id=create_order_dto.customer_id,
            restaurant_id=create_order_dto.restaurant_id,
            promo_code_id=create_order_dto.promo_code_id,
            status=create_order_dto.status.value,
            items_total=create_order_dto.items_total,
            delivery_fee=create_order_dto.delivery_fee,
            tax_fee=create_order_dto.tax_fee,
            final_amount=create_order_dto.final_amount,
            address_id=create_order_dto.address_id,
        )

        return self._convert_to_order_dto(order_obj=order_obj)

    def create_order_items(self, order_item_dtos: List[CreateOrderItemDTO]):
        order_items = [
            OrderItem(
                order_id=each.order_id,
                item_id=each.item_id,
                quantity=each.quantity,
                item_price=each.item_price,
            )
            for each in order_item_dtos
        ]

        OrderItem.objects.bulk_create(order_items)

    def update_order_status(
        self, order_id: str, status: OrderStatus
    ) -> OrderDTO | None:
        Order.objects.filter(id=order_id).update(status=status.value)

        return self.get_order(order_id=order_id)

    def get_user_orders(self, user_id: str, limit: int, offset: int) -> List[OrderDTO]:
        user_order_objs = Order.objects.filter(customer_id=user_id).order_by(
            "-created_at"
        )[offset : offset + limit]

        return [self._convert_to_order_dto(order_obj=each) for each in user_order_objs]

    # TODO: .get() raises uncaught DoesNotExist. Also dead code — callers already have placed_at on the DTO.
    def get_order_placed_at(self, order_id: str) -> datetime:
        order_obj = Order.objects.get(id=order_id)

        return order_obj.created_at

    def get_restaurant_orders(
        self,
        restaurant_id: str,
        limit: int,
        offset: int,
    ) -> List[OrderDTO]:

        order_objs = (
            Order.objects.filter(restaurant_id=restaurant_id)
            .exclude(status=OrderStatus.CANCELLED.value)
            .order_by("-created_at")
        )[offset : offset + limit]

        return [self._convert_to_order_dto(order_obj=each) for each in order_objs]

    # TODO: get_restaurant_orders excludes CANCELLED but this method doesn't — inconsistent restaurant-owner feed.
    def get_today_restaurant_orders(
        self, restaurant_id: str, limit: int, offset: int
    ) -> List[OrderDTO]:

        # TODO: date.today() is naive but created_at is tz-aware — drops/dupes orders near midnight. Use timezone.localdate().
        today = date.today()

        orders = Order.objects.filter(
            restaurant_id=restaurant_id,
            created_at__date=today,
        ).order_by("-created_at")[offset : offset + limit]

        return [self._convert_to_order_dto(order_obj=order) for order in orders]

    def get_restaurant_orders_summary(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> RestaurantOrdersSummaryDTO:
        orders = Order.objects.filter(
            restaurant_id=restaurant_id,
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
        )

        result = orders.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum(
                "final_amount",
                filter=~Q(status=OrderStatus.CANCELLED.value),
            ),
            avg_order_value=Avg(
                "final_amount",
                filter=~Q(status=OrderStatus.CANCELLED.value),
            ),
            total_cancelled=Count(
                "id",
                filter=Q(status=OrderStatus.CANCELLED.value),
            ),
        )

        total_orders = result["total_orders"] or 0
        total_cancelled = result["total_cancelled"] or 0
        total_revenue = Decimal(str(result["total_revenue"] or 0))
        avg_order_value = Decimal(str(result["avg_order_value"] or 0))

        cancellation_rate = (
            Decimal(str(total_cancelled)) / Decimal(str(total_orders)) * 100
            if total_orders > 0
            else Decimal("0.00")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return RestaurantOrdersSummaryDTO(
            total_orders=total_orders,
            total_revenue=total_revenue.quantize(Decimal("0.01")),
            avg_order_value=avg_order_value.quantize(Decimal("0.01")),
            total_cancelled=total_cancelled,
            cancellation_rate=cancellation_rate,
        )

    def get_orders_count_by_status(
        self, restaurant_id: str, date_from: date, date_to: date
    ) -> List[OrdersByStatusDTO]:
        results = (
            Order.objects.filter(
                restaurant_id=restaurant_id,
                created_at__date__gte=date_from,
                created_at__date__lte=date_to,
            )
            .values("status")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return [
            OrdersByStatusDTO(
                status=row["status"],
                count=row["count"],
            )
            for row in results
        ]

    def get_top_selling_items(
        self,
        restaurant_id: str,
        date_from: date,
        date_to: date,
    ) -> List[TopSellingItemDTO]:

        results = (
            OrderItem.objects.filter(
                order__restaurant_id=restaurant_id,
                order__created_at__date__gte=date_from,
                order__created_at__date__lte=date_to,
                order__status=OrderStatus.DELIVERED.value,
            )
            .values("item_id")
            .annotate(
                quantity_sold=Sum("quantity"),
                # TODO: DecimalField() has no max_digits/decimal_places — risk of precision loss.
                revenue=Sum(
                    ExpressionWrapper(
                        F("item_price") * F("quantity"),
                        output_field=DecimalField(),
                    )
                ),
            )
            .order_by("-quantity_sold")[:5]  # TODO: magic number 5 — undocumented limit, not in the interface contract.
        )

        return [
            TopSellingItemDTO(
                menu_item_id=str(row["item_id"]),
                quantity_sold=row["quantity_sold"],
                revenue=Decimal(str(row["revenue"] or 0)).quantize(Decimal("0.01")),
            )
            for row in results
        ]

    def get_peak_hours(
        self,
        restaurant_id: str,
        date_from: date,
        date_to: date,
    ) -> List[PeakHourDTO]:

        results = (
            Order.objects.filter(
                restaurant_id=restaurant_id,
                created_at__date__gte=date_from,
                created_at__date__lte=date_to,
            )
            .annotate(hour=ExtractHour("created_at"))
            .values("hour")
            .annotate(order_count=Count("id"))
            .order_by("hour")
        )

        return [
            PeakHourDTO(
                hour=row["hour"],
                order_count=row["order_count"],
            )
            for row in results
        ]

    def get_orders_items(self, order_ids: List[str]) -> List[OrderItemDTO]:
        order_item_objs = OrderItem.objects.filter(order_id__in=order_ids)

        return [
            OrderItemDTO(
                order_id=obj.order.id, # TODO: this triggers a query per row (N+1). Use obj.order_id (FK column is already loaded).
                item_id=obj.item_id,
                quantity=obj.quantity,
                item_price=obj.item_price,
                subtotal=Decimal(str(obj.item_price * obj.quantity)),
            )
            for obj in order_item_objs
        ]
