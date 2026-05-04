from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Project, ProjectCategory, ProjectReview, ProjectRating, Favorite
from .forms import ProjectForm, ProjectUpdateForm,ProjectReviewForm


def project_list(request):
    project = Project.objects.all()

    return render(request, 'diyprojects/diyprojects_list.html', {"project" : project})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # favorite = project.favorites.count()
    # ratings = project

    return render(request, 'diyprojects/diyprojects_detail.html', {"project" : project})
        

class ProjectAddView(CreateView):
    model = Project
    template_name = 'diyprojects/diyprojects_add.html'
    form_class = ProjectForm


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'diyprojects/diyprojects_update.html'
    form_class = ProjectUpdateForm
