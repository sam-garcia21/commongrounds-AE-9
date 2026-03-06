from django.shortcuts import redirect, render
from .models import Product


def item_list(request):
    items = Product.objects.all()
    return render(request, "merchstore/item_list.html", {"items": items})


def item_detail(request, id):
    item = Product.objects.get(id=id)
    return render(request, "merchstore/item_detail.html", {"item": item})

def home(request):
    return redirect("/merchstore/items")