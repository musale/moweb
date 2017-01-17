"""Views file for core app."""
from django.views.generic import TemplateView


class LandingPage(TemplateView):
    """The landing page."""

    template_name = "core/index.html"
