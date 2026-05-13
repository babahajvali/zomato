import uuid

from django.db import models

from accounts.constants.enums import Role


class User(models.Model):
    # TODO: use UUIDField instead of CharField(36) for UUID PKs (indexing/perf, matches other apps).
    id = models.CharField(
        max_length=36, primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    # TODO: max_length=255 is too lax for a phone number — add a regex validator.
    phone_number = models.CharField(max_length=255)
    # TODO: Role is a plain Enum — using models.TextChoices removes the custom get_list_of_tuples helper.
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
    pin_code = models.CharField(max_length=10) # TODO: rename -> pincode and why is it charfield?
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

    class Meta:
        unique_together = ("user", "label")
