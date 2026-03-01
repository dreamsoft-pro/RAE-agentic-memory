"""
URL patterns for the configurator web interface.

These routes render HTML pages for uploading screenshots and drawing
regions of interest. API routes are defined separately in
``api_urls.py``.
"""
from __future__ import annotations

from django.urls import path

from . import views

app_name = 'configurator'

urlpatterns = [
    path('', views.setup_app, name='setup_app'),
    path('application/<int:pk>/', views.configure_app, name='configure_app'),
]