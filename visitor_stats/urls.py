from django.urls import path

from . import views

urlpatterns = [
    path('', views.visitor_stats, name='visitor_stats'),
]
