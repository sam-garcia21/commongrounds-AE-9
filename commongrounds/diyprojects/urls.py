from django.urls import path
from django.views.generic.edit import CreateView, UpdateView

from .views import ProjectListView, ProjectDetailView, ProjectAddView, ProjectUpdateView


urlpatterns = [
    path('projects', ProjectListView.as_view(), name='diyprojects_list'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='diyprojects_detail'),
    path('project/add', ProjectAddView.as_view(), name='diyprojects_add'),
    path('project/<int:pk>/edit', ProjectUpdateView.as_view(), name='diyprojects_update'),

]

app_name = "diyprojects"