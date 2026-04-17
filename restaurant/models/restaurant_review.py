from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from restaurant.models.restaurant import Restaurant


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer = models.ForeignKey("account.User", on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.customer} - {self.rating}"

    class Meta:
        unique_together = (('restaurant', 'customer'),)

