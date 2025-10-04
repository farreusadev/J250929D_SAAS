"""
Landing Page Views
"""
from django.shortcuts import render


def landing_page(request):
    """
    Landing page view - Homepage del sitio
    """
    return render(request, 'landing_page/landing.html')
