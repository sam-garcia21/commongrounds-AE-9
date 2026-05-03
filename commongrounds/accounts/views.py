from django.shortcuts import render
from django.views.generic.edit import UpdateView 
from .models import Profile 
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile 
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile 

    def get_success_url(self):
        return reverse_lazy('accounts:profile_detail', kwargs={'username': self.request.user.username})