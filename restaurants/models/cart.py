import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Cart(models.Model):
    id = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False, primary_key=True
    )
    customer_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_id

    class Meta:
        indexes = [models.Index(fields=["customer_id"])]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey("MenuItem", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    # TODO: default=0.0 is a float — use Decimal("0.00") to avoid precision loss.
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_item.name

    class Meta:
        unique_together = ("cart", "menu_item")
