from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Project, ProjectCategory, ProjectReview, ProjectRating, Favorite
from .forms import ProjectForm, ProjectUpdateForm


def project_list(request):
    project = Project.objects.all()
    created = []
    favorited = []
    reviewed = []

    if request.user.is_authenticated:
        viewer = request.user.profile
        created = Project.objects.filter(profile=viewer)
        favorited = Project.objects.filter(favorites__profile=viewer)
        reviewed = Project.objects.filter(reviews__reviewer=viewer)

        project = project.exclude(profile=viewer)
        project = project.exclude(favorites__profile=viewer)
        project = project.exclude(reviews__reviewer=viewer).distinct()

    return render(request, 'diyprojects/diyprojects_list.html', {
        "project": project,
        "created": created,
        "favorited": favorited,
        "reviewed": reviewed,
    }
    )


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    favorite_count = project.favorites.count()
    rating = project.ratings.all()
    review = project.reviews.all()

    if project.ratings.count() != 0:
        i = 0
        for r in rating:
            i += r.score
        avg_rating = i//project.ratings.count()
    else:
        avg_rating = 0

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'favorite' and request.user.is_authenticated:
            favorite, created = Favorite.objects.get_or_create(
                project=project,
                profile=request.user.profile,
            )
            if not created:
                favorite.delete()

        elif action == 'review':
            comment = request.POST.get('comment')
            image = request.FILES.get('image')
            user_profile = request.user.profile

            ProjectReview.objects.create(
                project=project,
                reviewer=request.user.profile,
                comment=comment,
                image=image)

        elif action == 'rate':
            ProjectRating.objects.create(
                project=project,
                profile=request.user.profile,
                score=request.POST.get('score'))

        return redirect('diyprojects:diyprojects_detail', pk=project.pk)

    can_update = False
    if request.user.is_authenticated and project.profile == request.user.profile:
        can_update = True

    return render(request, 'diyprojects/diyprojects_detail.html', {
        "project": project,
        "favorite_count": favorite_count,
        "rating": rating,
        "review": review,
        "avg_rating": avg_rating,
        "can_update": can_update,
    })


@login_required
def project_create(request):
    project_maker = request.user.profile

    if request.user.profile.role != "Project Creator":
        raise PermissionDenied

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = project_maker
            project.save()
            return redirect('diyprojects:diyprojects_detail', pk=project.pk)
    else:
        form = ProjectForm()

    return render(request, "diyprojects/diyprojects_add.html", {
        "form": form,
        "project_maker": project_maker,
    })


@login_required
def project_update(request, pk):
    if request.user.profile.role != "Project Creator":
        raise PermissionDenied

    project = get_object_or_404(Project, pk=pk)

    if request.method == "POST":
        form = ProjectUpdateForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('diyprojects:diyprojects_detail', pk=project.pk)
    else:
        form = ProjectUpdateForm(instance=project)

    return render(request, "diyprojects/diyprojects_update.html", {"form": form})
