from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns for your application
    path('analytics_dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
]
