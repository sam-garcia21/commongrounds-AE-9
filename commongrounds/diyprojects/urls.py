from django.urls import path
from django.views.generic.edit import CreateView, UpdateView

from .views import project_detail, project_list, ProjectAddView, ProjectUpdateView


urlpatterns = [
    path('projects', project_list, name='diyprojects_list'),
    path('project/<int:pk>', project_detail, name='diyprojects_detail'),
    path('project/add', ProjectAddView.as_view(), name='diyprojects_add'),
    path('project/<int:pk>/edit', ProjectUpdateView.as_view(), name='diyprojects_update'),

]

app_name = "diyprojects"