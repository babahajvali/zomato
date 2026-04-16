import uuid

from django.db import models
from .enums import Role


# Create your models here.


class User(models.Model):


    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=10, choices=Role.get_list_of_tuples())
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    full_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.label

    
    