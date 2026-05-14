from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(
        "restaurants.Restaurant", models.CASCADE, related_name="restaurant_reviews"
    )
    customer_id = models.CharField(max_length=255)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rating}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["restaurant", "customer_id"],
                name="unique_restaurant_review",
            )
        ]
