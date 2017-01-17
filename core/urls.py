"""Core URL configguration."""

from django.conf.urls import url

from core.views import LandingPage

urlpatterns = [
    url(r'$', LandingPage.as_view(), name='LandingPage'),
]
