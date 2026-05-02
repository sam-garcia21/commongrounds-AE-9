from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Project, ProjectCategory
from .forms import ProjectForm, ProjectUpdateForm


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/diyprojects_list.html'
    

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/diyprojects_detail.html'


class ProjectAddView(CreateView):
    model = Project
    template_name = 'diyprojects/diyprojects_add.html'
    form_class = ProjectForm


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'diyprojects/diyprojects_update.html'
    form_class = ProjectUpdateForm
