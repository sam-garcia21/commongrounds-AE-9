from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Project, ProjectCategory

class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/diyprojects_list.html'
    

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/diyprojects_detail.html'
