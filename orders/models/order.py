import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from orders.constants.enums import OrderStatus


class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=uuid.uuid4)
    customer_id = models.CharField(max_length=255)
    restaurant_id = models.CharField(max_length=255)
    promo_code = models.ForeignKey(
        "PromoCode", on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.CharField(
        max_length=255,
        choices=OrderStatus.get_list_of_tuples(),
        default=OrderStatus.PLACED,
    )
    items_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tax_fee = models.DecimalField(max_digits=10, decimal_places=2)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant_id} - {self.customer_id}"

    class Meta:
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
