from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView 
from .models import Profile 
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import ProfileUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile

from bookclub.models import Book
from commissions.models import Commission
from diyprojects.models import Project
from localevents.models import Event
from merchstore.models import Product

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


def dashboard(request):
    book_list = []
    commission_list = []
    project_list = []
    product_list = []
    event_list = []
    

    if request.user.is_authenticated:
        viewer = request.user.profile
        book_list = Book.objects.filter(contributor=viewer)
        commission_list = Commission.objects.filter(maker=viewer)
        project_list = Project.objects.filter(profile=viewer)
        product_list = Product.objects.filter(owner=viewer)
        #event_list = Product.objects.filter(owner=viewer)


    return render(request, 'accounts/dashboard.html', {
        "book_list" : book_list,
        "commission_list" : commission_list,
        "project_list" : project_list,
        "product_list" : product_list,
        "event_list" : event_list,
        }
    )