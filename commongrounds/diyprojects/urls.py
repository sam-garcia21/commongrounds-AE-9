from django.urls import path

from .views import ProjectListView, ProjectDetailView

urlpatterns = [
    path('diyprojects/projects', ProjectListView.as_view(), name='diyprojects_list'),
    path('diyprojects/project/<int:pk>',
         ProjectDetailView.as_view(), name='diyprojects_detail'),
]

app_name = "diyprojects"
