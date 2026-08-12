from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import uuid

from .models import Sale, Quotation, SaleItem
from .forms import SaleForm, SaleItemFormSet


@login_required(login_url="login")
def sale_list(request):
    sales = Sale.objects.all().order_by("-sale_date")

    status_filter = request.GET.get("payment_status", "")
    if status_filter:
        sales = sales.filter(payment_status=status_filter)

    return render(request, "sales/list.html", {
        "sales": sales,
        "status_filter": status_filter,
    })


@login_required(login_url="login")
def sale_add(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        formset = SaleItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            sale = form.save(commit=False)
            sale.sales_employee = request.user
            sale.save()
            formset.instance = sale
            formset.save()
            messages.success(request, "Sale recorded successfully.")
            return redirect("sale_detail", pk=sale.pk)
    else:
        initial = {"invoice_number": f"INV-{uuid.uuid4().hex[:8].upper()}"}
        form = SaleForm(initial=initial)
        formset = SaleItemFormSet()
    return render(request, "sales/form.html", {
        "form": form, "formset": formset, "title": "Record Sale",
    })


@login_required(login_url="login")
def sale_from_quotation(request, quotation_pk):
    """Quotation -> Accepted -> Sale flow (matches the PDF's business flow diagram)."""
    quotation = get_object_or_404(Quotation, pk=quotation_pk)

    if request.method == "POST":
        if quotation.status != "accepted":
            quotation.status = "accepted"
            quotation.save()

        sale = Sale.objects.create(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            customer=quotation.customer,
            quotation=quotation,
            discount=quotation.discount,
            gst=quotation.gst,
            sales_employee=request.user,
        )
        for item in quotation.items.all():
            SaleItem.objects.create(
                sale=sale,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
            )
        messages.success(request, f"Sale created from quotation: {sale.invoice_number}")
        return redirect("sale_detail", pk=sale.pk)

    return render(request, "sales/confirm_from_quotation.html", {"quotation": quotation})


@login_required(login_url="login")
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, "sales/detail.html", {"sale": sale})


@login_required(login_url="login")
def sale_delete(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        sale.delete()
        messages.success(request, "Sale deleted.")
        return redirect("sale_list")
    return render(request, "sales/confirm_delete.html", {"sale": sale})
