from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ActivityLog


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'discord_username')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'status'),
        }),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Online Status', {'fields': ('is_online', 'last_seen')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'role', 'status', 'is_online', 'created_at')
    list_filter = ('role', 'status', 'is_active', 'is_online', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'last_seen')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'user__email', 'action')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp', 'user', 'action', 'details', 'ip_address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
