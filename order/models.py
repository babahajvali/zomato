from django.db import models

from order.enums import PromoCodeType


# Create your models here.


class PromoCode(models.Model):
    code = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=30, choices=PromoCodeType.get_list_of_tuples())
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_usage = models.IntegerField()
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.code

    