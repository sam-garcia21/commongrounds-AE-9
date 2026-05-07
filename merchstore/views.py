from django.shortcuts import redirect, render
from .models import Product, Transaction
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, TransactionForm
from collections import defaultdict
from .strategies import AuthenticatedPurchaseStrategy, GuestPurchaseStrategy


def item_list(request):
    items = Product.objects.all()
    return render(request, "merchstore/item_list.html", {"items": items})


def item_detail(request, id):
    product = Product.objects.get(id=id)

    form = TransactionForm()

    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                strategy = AuthenticatedPurchaseStrategy()
            else:
                strategy = GuestPurchaseStrategy()

        return strategy.execute(request, product, form)
    return render(request, "merchstore/item_detail.html", {
        "product": product,
        "form": form,
    })


def home(request):
    return redirect("/merchstore/items")


@login_required
def product_create(request):
    if request.user.profile.role != "Market Seller":
        return redirect('/merchstore/items')
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user.profile
            product.save()
            return redirect(f"/merchstore/item/{product.id}")
    else:
        form = ProductForm()

    return render(request, "merchstore/product_form.html", {"form": form})

    



@login_required
def product_update(request, id):
    if request.user.profile.role != "Market Seller":
        return redirect('/merchstore/items')
    product = Product.objects.get(id=id)

    if product.owner != request.user.profile:
        return redirect('/merchstore/items')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)

            if updated_product.stock == 0:
                updated_product.status = 'out'
            else:
                updated_product.status = 'available'

            updated_product.save()
            return redirect(f"/merchstore/item/{product.id}")
    else:
        form = ProductForm(instance=product)

        return render(request, "merchstore/product_form.html", {"form": form})


    return render(request, "merchstore/product_form.html", {"form": form}) 

@login_required
def cart_view(request):
    transactions = Transaction.objects.filter(buyer=request.user.profile)

    return render(request, "merchstore/cart.html", {
        "transactions": transactions
    })



@login_required
def transactions_view(request):
    transactions = Transaction.objects.filter(
        product__owner=request.user.profile)

    grouped = defaultdict(list)

    for t in transactions:
        grouped[t.buyer].append(t)

    return render(request, "merchstore/transactions.html", {
        "grouped_transactions": dict(grouped)
    })


@login_required
def cart_view(request):
    transactions = Transaction.objects.filter(buyer=request.user.profile)

    grouped = defaultdict(list)

    for t in transactions:
        grouped[t.product.owner].append(t)

    return render(request, "merchstore/cart.html", {
        "grouped_transactions": dict(grouped)
    })

    return render(request, "merchstore/product_form.html", {"form": form})
