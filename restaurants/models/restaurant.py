import uuid

from django.core.validators import MinValueValidator
from django.db import models

from restaurants.constants.enums import CuisineType, Category


# Create your models here.


class Restaurant(models.Model):
    id = models.CharField(
        max_length=36, default=uuid.uuid4, editable=False, primary_key=True
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    owner_id = models.CharField(max_length=255)
    cuisine_type = models.CharField(
        max_length=255, choices=CuisineType.get_list_of_tuples()
    )
    address = models.TextField()
    pin_code = models.CharField(max_length=6)
    is_veg_only = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["is_deleted", "cuisine_type"]),
            models.Index(fields=["is_deleted", "pin_code", "name"]),
            models.Index(fields=["is_deleted", "cuisine_type", "name"]),
        ]


class MenuItem(models.Model):
    id = models.CharField(
        max_length=36, default=uuid.uuid4(), editable=False, primary_key=True
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menu_items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30, choices=Category.get_list_of_tuples())
    is_veg = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    preparation_time_in_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "name"],
                name="unique_menu_item_per_restaurant",
            )
        ]
