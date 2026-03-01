"""
URL routing for the statistics app.
"""
from __future__ import annotations

from django.urls import path

from . import views

app_name = 'statistics'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('roi/<int:roi_id>/data/', views.roi_data_json, name='roi-data-json'),
]