from django.contrib import admin

from restaurants.models import (
    Cart,
    CartItem,
    DeliveryZone,
    MenuItem,
    Restaurant,
    RestaurantReview,
    RestaurantTiming,
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner_id",
        "cuisine_type",
        "is_veg_only",
        "is_deleted",
        "created_at",
    )
    list_filter = ("cuisine_type", "is_veg_only", "is_deleted", "created_at")
    search_fields = ("name", "address")
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "owner_id", "cuisine_type")},
        ),
        ("Location Information", {"fields": ("address", "pin_code")}),
        ("Settings", {"fields": ("is_veg_only", "is_deleted")}),
        (
            "System Information",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ("created_at", "updated_at")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "restaurant",
        "category",
        "price",
        "is_veg",
        "is_available",
        "preparation_time_in_minutes",
        "created_at",
    )
    list_filter = ("category", "is_veg", "is_available", "created_at", "updated_at")
    search_fields = ("name", "restaurant__name", "description")
    ordering = ("-created_at",)
    raw_id_fields = ("restaurant",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = (
        "restaurant",
        "pin_code",
        "delivery_fee",
        "estimated_delivery_mins",
        "created_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("restaurant__name", "pin_code")
    ordering = ("-created_at",)
    raw_id_fields = ("restaurant",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "item_id",
        "restaurant",
        "customer_id",
        "rating",
        "created_at",
    )
    list_filter = ("rating", "created_at")
    search_fields = ("item_id", "restaurant__name", "customer_id", "review_text")
    ordering = ("-created_at",)
    readonly_fields = (
        "item_id",
        "created_at",
    )


@admin.register(RestaurantTiming)
class RestaurantTimingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "restaurant",
        "day_of_week",
        "open_time",
        "close_time",
        "created_at",
    )
    list_filter = ("day_of_week", "created_at", "updated_at")
    search_fields = ("restaurant__name",)
    ordering = ("restaurant", "day_of_week")
    raw_id_fields = ("restaurant",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_id", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "customer_id")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cart",
        "menu_item",
        "quantity",
        "item_price",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("cart__id", "cart__customer_id", "menu_item__name")
    ordering = ("-created_at",)
    raw_id_fields = ("cart", "menu_item")
    readonly_fields = ("created_at", "updated_at")
