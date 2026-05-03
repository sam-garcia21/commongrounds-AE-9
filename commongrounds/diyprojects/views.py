from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Project, ProjectCategory, ProjectReview, ProjectRating, Favorite
from .forms import ProjectForm, ProjectUpdateForm,ProjectReviewForm


class ProjectListView(ListView):
    model = Project
    template_name = 'diyprojects/diyprojects_list.html'
    

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'diyprojects/diyprojects_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = ProjectReview.objects.all()
        context["favorite"] = Favorite.objects.all()
        context["form"] = ProjectReviewForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProjectReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return self.get(request, *args, **kwargs)
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)
        

class ProjectAddView(CreateView):
    model = Project
    template_name = 'diyprojects/diyprojects_add.html'
    form_class = ProjectForm


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'diyprojects/diyprojects_update.html'
    form_class = ProjectUpdateForm
