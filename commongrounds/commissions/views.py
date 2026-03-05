from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Commission

# Create your views here.


class CommissionDetailView(DetailView):
    model = Commission
    template_name = "commission_detail.html"


class CommissionListView(ListView):
    model = Commission
    template_name = "commission_list.html"