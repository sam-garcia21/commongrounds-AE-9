from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView
from .models import Profile
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .forms import ProfileUpdateForm, RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.contrib.auth import login

from bookclub.models import Book
from commissions.models import Commission
from diyprojects.models import Project
from localevents.models import Event
from merchstore.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def homepage(request):
    return render(request, 'accounts/homepage.html')


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
        event_list = Event.objects.filter(organizer=viewer)

    return render(request, 'accounts/dashboard.html', {
        "book_list": book_list,
        "commission_list": commission_list,
        "project_list": project_list,
        "product_list": product_list,
        "event_list": event_list,
    }
    )


def register(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
