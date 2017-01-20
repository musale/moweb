"""Core URL configguration."""

from django.conf.urls import url

from core.views import ItemView, LandingPage

urlpatterns = [
    url(r'^$', LandingPage.as_view(), name='LandingPage'),
    url(r'^item/(?P<id>[0-9]+)/$', ItemView.as_view(), name='item'),
]
