from django.urls import path
from . import views

app_name = "merchstore"

urlpatterns = [
    path('', views.home),
    path("items", views.item_list, name="item_list"),
    path("item/<int:id>", views.item_detail, name="item_detail"),
    path('item/add', views.product_create),
    path('item/<int:id>/edit', views.product_update),
    path('cart', views.cart_view),
    path('transactions', views.transactions_view),
]
