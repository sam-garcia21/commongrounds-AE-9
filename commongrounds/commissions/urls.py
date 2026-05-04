from django.urls import path

from .views import CommissionListView, CommissionDetailView, CommissionCreateView

urlpatterns = [
    path('requests/', CommissionListView.as_view(), name='commission_list'),
    path('request/<int:pk>/', CommissionDetailView.as_view(),
         name='commission_detail'),
    path('requests/add', CommissionCreateView.as_view(), name='commission_create')
]

app_name = 'commissions'
