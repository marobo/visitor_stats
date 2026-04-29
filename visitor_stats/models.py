from django.db import models
from django.utils import timezone


class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    page = models.CharField(max_length=500)
    user_agent = models.TextField(blank=True)
    visited_at = models.DateTimeField(default=timezone.now)

    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['-visited_at']

    def __str__(self):
        return f"{self.ip_address} - {self.page}"
