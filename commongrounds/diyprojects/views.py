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
    favorite_count = project.favorites.count()
    rating = project.ratings.all()
    review = project.reviews.all

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'favorite': #and request.user.is_authenticated:
            project, created = Favorite.objects.get_or_create(
                project=project,
                #profile=request.user.profile
                )
            if not created:
                project.delete()

        elif action == 'review':
            comment = request.POST.get('comment')
            #user_profile = request.user.profile

            ProjectReview.objects.create(
                project=project, 
                #reviewer=user_profile,
                comment=comment)
            
        elif action == 'rate':
            ProjectRating.objects.create(
                project=project, 
                #profile=user_profile,
                score=request.POST.get('score'))

        return redirect('diyprojects:diyprojects_detail', pk=project.pk)



    return render(request, 'diyprojects/diyprojects_detail.html', {
        "project" : project,
        "favorite_count" : favorite_count,
        "rating" : rating,
        "review" : review,
    })
        

class ProjectAddView(CreateView):
    model = Project
    template_name = 'diyprojects/diyprojects_add.html'
    form_class = ProjectForm
    template_name = 'diyprojects/diyprojects_list.html'


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'diyprojects/diyprojects_update.html'
    form_class = ProjectUpdateForm
