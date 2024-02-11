from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

from django.contrib.auth import logout

class UserRegistrationView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/user_registration.html'

    def get_success_url(self):
        return reverse('blueblogs:home')
    
class CustomLogoutView():
    template_name = 'accounts/logout.html'

    def logout_user(request):
        logout(request)
        return render(request, 'accounts/logout.html', {})

    