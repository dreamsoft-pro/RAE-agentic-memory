"""
Forms for the configurator app.

Provides a simple form to upload an application screenshot and assign a name.
"""
from __future__ import annotations

from django import forms
from .models import TrackedApplication


class TrackedApplicationForm(forms.ModelForm):
    class Meta:
        model = TrackedApplication
        fields = ['name', 'screenshot']