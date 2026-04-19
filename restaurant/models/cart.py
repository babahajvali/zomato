import uuid

from django.db import models


class Cart(models.Model):
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    customer = models.OneToOneField("account.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.name


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu_item = models.ForeignKey("MenuItem", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.menu_item.name

    class Meta:
        unique_together = ('cart', 'menu_item')