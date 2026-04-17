from django.contrib import admin

from restaurant.models.restaurant import Restaurant


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
