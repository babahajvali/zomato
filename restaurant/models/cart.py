import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from utils.uuid_util import generate_uuid


class Cart(models.Model):
    id = models.CharField(
        max_length=36,
        default=generate_uuid(),
        editable=False,
        primary_key=True
    )
    customer_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_id

    class Meta:
        unique_together = ('id', 'customer_id')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey("MenuItem", on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_item.name

    class Meta:
        unique_together = ('cart', 'menu_item')
