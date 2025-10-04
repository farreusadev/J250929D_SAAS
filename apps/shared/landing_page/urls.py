"""
Landing Page URLs
"""
from django.urls import path
from . import views

app_name = "landing_page"

urlpatterns = [
    path("", views.landing_page, name="home"),
]