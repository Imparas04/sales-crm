from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Product
from .decorators import role_required
from .forms import ProductForm


@login_required(login_url="login")
def product_list(request):
    products = Product.objects.all().order_by("-created_at")

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        )

    status_filter = request.GET.get("status", "")
    if status_filter:
        products = products.filter(status=status_filter)

    return render(request, "products/list.html", {
        "products": products,
        "query": query,
        "status_filter": status_filter,
    })


@login_required(login_url="login")
@role_required("admin", "manager")
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/form.html", {"form": form, "title": "Add Product"})


@login_required(login_url="login")
@role_required("admin", "manager")
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "products/form.html", {"form": form, "title": "Edit Product"})


@login_required(login_url="login")
@role_required("admin", "manager")
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("product_list")
    return render(request, "products/confirm_delete.html", {"product": product})
