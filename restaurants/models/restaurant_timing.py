from django.db import models

from restaurants.models.restaurant import Restaurant


class RestaurantTiming(models.Model):
    DAY_CHOICES = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant.name

    class Meta:
        unique_together = ("restaurant", "day_of_week")
