from django.urls import path
from . import views

app_name = "localevents"

urlpatterns = [
    path('events', views.event_list, name='event-list'),
    path('event/<int:pk>', views.event_detail, name='event-detail'),
    path('event/add', views.event_create, name='event-add'),
    path('event/<int:pk>/edit', views.event_update, name='event-edit'),
    path('event/<int:pk>/signup', views.event_signup, name='event-signup'),
]
