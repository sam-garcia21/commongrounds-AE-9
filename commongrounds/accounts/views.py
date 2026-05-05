from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView 
from .models import Profile 
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile 
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_form.html'

    def get_object(self):
        url_username = self.kwargs.get('username')
        user_get = get_object_or_404(User, username=url_username)
        if self.request.user.username != url_username:
            raise PermissionDenied
        profile, created = Profile.objects.get_or_create(user=user_get)
        return profile 

    def get_success_url(self):
        return reverse_lazy('accounts:profile_update', kwargs={'username': self.request.user.username})