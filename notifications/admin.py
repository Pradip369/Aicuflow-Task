from django.contrib import admin
from notifications.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'sender',
        'receiver',
        'title',
        'is_read',
        'created_at',
    )
    list_filter = ('is_read', 'title', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'title', 'message')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Notification Info', {
            'fields': ('sender', 'receiver', 'title', 'message', 'is_read')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
