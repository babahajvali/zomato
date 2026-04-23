from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", models.CASCADE, related_name="restaurant_reviews"
    )
    item_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    customer_id = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}"

    class Meta:
        unique_together = (("restaurant", "customer_id"),)
