"""
Web interface views for the configurator app.

These views allow administrators to upload screenshots for tracked applications
and to define regions of interest interactively. The ROI creation is
delegated to JavaScript in the frontend, which posts data to the API.
"""
from __future__ import annotations

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import TrackedApplicationForm
from .models import TrackedApplication


def setup_app(request):
    """Display a form to create new tracked applications and list existing ones."""
    apps = TrackedApplication.objects.all().order_by('name')
    if request.method == 'POST':
        form = TrackedApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('configurator:setup_app'))
    else:
        form = TrackedApplicationForm()
    return render(request, 'configurator/setup_app.html', {'form': form, 'apps': apps})


def configure_app(request, pk: int):
    """Render a page showing the uploaded screenshot to allow ROI selection."""
    application = get_object_or_404(TrackedApplication, pk=pk)
    return render(request, 'configurator/configure_app.html', {'application': application})