from django.urls import path
from django.views.generic.edit import CreateView, UpdateView

from .views import project_detail, project_list, project_create, project_update


urlpatterns = [
    path('projects', project_list, name='diyprojects_list'),
    path('project/<int:pk>', project_detail, name='diyprojects_detail'),
    path('project/add', project_create, name='diyprojects_add'),
    path('project/<int:pk>/edit', project_update, name='diyprojects_update'),
]

app_name = "diyprojects"
