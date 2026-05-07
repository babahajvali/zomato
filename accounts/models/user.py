import uuid

from django.db import models

from accounts.constants.enums import Role


class User(models.Model):
    id = models.CharField(
        max_length=36, primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=Role.get_list_of_tuples())
    password = models.CharField(max_length=255, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    full_address = models.TextField()
    city = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

    class Meta:
        unique_together = ("user", "label")
