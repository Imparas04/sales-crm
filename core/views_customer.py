from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Customer
from .forms import CustomerForm


@login_required(login_url="login")
def customer_list(request):
    customers = Customer.objects.all().order_by("-created_at")

    # Search
    query = request.GET.get("q", "").strip()
    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )

    # Filter
    status_filter = request.GET.get("status", "")
    if status_filter:
        customers = customers.filter(status=status_filter)

    return render(request, "customers/list.html", {
        "customers": customers,
        "query": query,
        "status_filter": status_filter,
    })


@login_required(login_url="login")
def customer_add(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully.")
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "customers/form.html", {"form": form, "title": "Add Customer"})


@login_required(login_url="login")
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully.")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/form.html", {"form": form, "title": "Edit Customer"})


@login_required(login_url="login")
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect("customer_list")
    return render(request, "customers/confirm_delete.html", {"customer": customer})


@login_required(login_url="login")
def customer_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "customers/detail.html", {"customer": customer})
