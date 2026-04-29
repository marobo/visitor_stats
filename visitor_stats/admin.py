from django.contrib import admin

from .models import Visitor


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = [
        'ip_address', 'country', 'city', 'device_type', 'browser', 'visited_at',
    ]
    list_filter = ['visited_at', 'device_type', 'country']
    search_fields = ['ip_address', 'country', 'city']
    readonly_fields = [
        'ip_address', 'user_agent', 'visited_at',
        'browser', 'operating_system', 'device_type', 'country', 'city',
        'latitude', 'longitude',
    ]
    date_hierarchy = 'visited_at'
