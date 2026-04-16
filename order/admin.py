from django.contrib import admin
from .models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'min_order_value', 'max_usage', 'is_valid', 'created_at')
    list_filter = ('discount_type', 'valid_from', 'valid_until', 'created_at')
    search_fields = ('code',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'discount_type', 'discount_value')
        }),
        ('Usage Limits', {
            'fields': ('min_order_value', 'max_usage')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at',)
    
    def is_valid(self, obj):
        from django.utils import timezone
        now = timezone.now()
        return obj.valid_from <= now <= obj.valid_until
    is_valid.boolean = True
    is_valid.short_description = 'Currently Valid'
