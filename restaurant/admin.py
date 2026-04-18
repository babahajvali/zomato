from django.contrib import admin

from restaurant.models import (
    DeliveryZone,
    MenuItem,
    Restaurant,
    RestaurantReview,
    RestaurantTiming,
)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('restaurant_id', 'name', 'owner', 'cuisine_type',
                    'is_veg_only', 'is_active', 'created_at')
    list_filter = ('cuisine_type', 'is_veg_only', 'is_active', 'created_at')
    search_fields = ('name', 'owner__name', 'address')
    ordering = ('-created_at',)
    raw_id_fields = ('owner',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'owner', 'cuisine_type')
        }),
        ('Location Information', {
            'fields': ('address', 'pin_code')
        }),
        ('Settings', {
            'fields': ('is_veg_only', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'item_id', 'name', 'restaurant', 'category', 'price', 'is_veg',
        'is_available', 'preparation_time_in_minutes', 'created_at'
    )
    list_filter = (
        'category', 'is_veg', 'is_available', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'restaurant__name', 'description')
    ordering = ('-created_at',)
    raw_id_fields = ('restaurant',)
    readonly_fields = ('item_id', 'created_at', 'updated_at')


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = (
        'restaurant', 'pin_code', 'delivery_fee', 'estimated_delivery_mins',
        'created_at'
    )
    list_filter = ('created_at', 'updated_at')
    search_fields = ('restaurant__name', 'pin_code')
    ordering = ('-created_at',)
    raw_id_fields = ('restaurant',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('restaurant__name', 'customer__name', 'review_text')
    ordering = ('-created_at',)
    raw_id_fields = ('restaurant', 'customer')
    readonly_fields = ('created_at',)


@admin.register(RestaurantTiming)
class RestaurantTimingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'restaurant', 'day_of_week', 'open_time', 'close_time',
        'created_at'
    )
    list_filter = ('day_of_week', 'created_at', 'updated_at')
    search_fields = ('restaurant__name',)
    ordering = ('restaurant', 'day_of_week')
    raw_id_fields = ('restaurant',)
    readonly_fields = ('created_at', 'updated_at')
