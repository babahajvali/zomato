from django.contrib import admin
from .models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'phone_number', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('name', 'email', 'user_id')
    ordering = ('-created_at',)
    readonly_fields = ('user_id', 'created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone_number', 'role')
        }),
        ('System Information', {
            'fields': ('user_id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('label', 'user', 'city', 'pin_code', 'is_default', 'created_at')
    list_filter = ('is_default', 'city', 'created_at')
    search_fields = ('label', 'user__name', 'city', 'full_address')
    ordering = ('-created_at',)
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Address Information', {
            'fields': ('user', 'label', 'full_address', 'city', 'pin_code', 'is_default')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
