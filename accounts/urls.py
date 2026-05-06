from django.urls import path, include
from .views import ProfileUpdateView, dashboard

app_name = "accounts"

urlpatterns = [
    path('dashboard/', dashboard, name="dashboard"),
    path('', include('django.contrib.auth.urls')),
    path('<str:username>/', ProfileUpdateView.as_view(), name='profile_update'),
]