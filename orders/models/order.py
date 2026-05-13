import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from orders.constants.enums import OrderStatus


# TODO: Where are we storing the discount applied on the order of a promo code.
class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4)
    # TODO: customer_id/restaurant_id are loose CharField with no FK — orphan-row risk and weak referential integrity.
    customer_id = models.CharField(max_length=255)
    restaurant_id = models.CharField(max_length=255)
    promo_code = models.ForeignKey(
        "PromoCode", on_delete=models.CASCADE, null=True, blank=True # TODO: in User the foreignkey is written differently.
    )
    status = models.CharField(
        max_length=255,
        choices=OrderStatus.get_list_of_tuples(),
        default=OrderStatus.PLACED,
    )
    items_total = models.DecimalField(max_digits=10, decimal_places=2)  # TODO: add units in the name
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address_id = models.CharField(max_length=255) # TODO: every DTO and the GraphQL type uses int — why is this a CharField? storage writes int into a string column.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant_id} - {self.customer_id}"

    class Meta:
        # TODO: missing composite indexes for hot queries — (restaurant_id, created_at), (customer_id, created_at), and promo_code for usage counts.
        indexes = [
            models.Index(fields=["restaurant_id"]),
            models.Index(fields=["status"]),
            models.Index(fields=["customer_id"]),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.CharField(max_length=255)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order} - {self.item_id}"

    class Meta:
        unique_together = (("order", "item_id"),)
