from django.core.validators import MinValueValidator
from django.db import models
import uuid

from restaurant.enums import CuisineType, Category


# Create your models here.

class Restaurant(models.Model):
    restaurant_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey("account.User", on_delete=models.CASCADE)
    cuisine_type = models.CharField(max_length=255, choices=CuisineType.get_list_of_tuples())
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    is_veg_only = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['owner']),
        ]


# class MenuItem(models.Model):
#     item_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     category = models.CharField(max_length=30,choices=Category.get_list_of_tuples())
#     is_veg = models.BooleanField(default=False)
#     is_available = models.BooleanField(default=True)
#     preparation_time_in_minutes = models.IntegerField(validators=[MinValueValidator(1)])
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     tags = models.JSONField(default=list, blank=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         indexes = [
#             models.Index(fields=['restaurant']),
#         ]