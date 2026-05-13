from django.contrib import admin
from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone_number",
        "role",
        "password",
        "created_at",
    )
    list_filter = ("role", "created_at")
    search_fields = ("name", "email", "id")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "email", "phone_number", "role", "password")},
        ),
        (
            "System Information",
            {"fields": ("id", "created_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "label",
        "user",
        "city",
        "pincode",
        "is_default",
        "created_at",
    )
    list_filter = ("is_default", "city", "created_at")
    search_fields = ("label", "user__name", "city", "full_address")
    ordering = ("-created_at",)
    raw_id_fields = ("user",)

    fieldsets = (
        (
            "Address Information",
            {
                "fields": (
                    "user",
                    "label",
                    "full_address",
                    "city",
                    "pincode",
                    "is_default",
                )
            },
        ),
        ("System Information", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
