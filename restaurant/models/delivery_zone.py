from django.core.validators import MinValueValidator
from django.db import models

from restaurant.models.restaurant import Restaurant


class DeliveryZone(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=6)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estimated_delivery_mins = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.pincode}"

    class Meta:
        unique_together = (('restaurant', 'pincode'),)
        indexes = [models.Index(fields=['restaurant']),]