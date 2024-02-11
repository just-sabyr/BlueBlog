"""Defines url patterns for blueblogs."""

from django.urls import path, include

# from django.views.generic import TemplateView
from .views import HomeView

app_name = 'blueblogs'
urlpatterns = [
    # Home url.
    # path('', homeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='home'),
]