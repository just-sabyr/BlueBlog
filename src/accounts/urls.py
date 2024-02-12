"""Defines url patterns for accounts."""

from django.urls import path, include

from .views import UserRegistrationView, CustomLogoutView
from django.contrib.auth.views import LoginView

app_name = 'accounts'
urlpatterns = [
    # Signup url.
    path('register/', UserRegistrationView.as_view(), name='register'),
    # Login url.
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Logout url.
    path('logout/', CustomLogoutView.logout_user, name='logout'),
]