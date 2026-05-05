from django.contrib import admin
from .models import Order, OrderItem, PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "discount_type",
        "discount_value",
        "min_order_value",
        "max_usage",
        "is_valid",
        "created_at",
    )
    list_filter = ("discount_type", "valid_from", "valid_until", "created_at")
    search_fields = ("code",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Information", {"fields": ("code", "discount_type", "discount_value")}),
        ("Usage Limits", {"fields": ("min_order_value", "max_usage")}),
        ("Validity Period", {"fields": ("valid_from", "valid_until")}),
        ("System Information", {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    readonly_fields = ("created_at",)

    def is_valid(self, obj):
        from django.utils import timezone

        now = timezone.localtime(timezone.now())

        return obj.valid_from <= now <= obj.valid_until

    is_valid.boolean = True
    is_valid.short_description = "Currently Valid"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_id",
        "restaurant_id",
        "promo_code_id",
        "status",
        "items_total",
        "delivery_fee",
        "tax_fee",
        "final_amount",
        "created_at",
        "scheduled_for",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("id", "customer_id", "restaurant_id", "address_id")
    ordering = ("-created_at",)
    raw_id_fields = ("promo_code",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "item_id", "quantity", "item_price", "created_at")
    list_filter = ("created_at",)
    search_fields = ("order__id", "item_id")
    ordering = ("-created_at",)
    raw_id_fields = ("order",)
    readonly_fields = ("created_at",)
