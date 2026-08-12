from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import Quotation
from .forms import QuotationForm, QuotationItemFormSet


@login_required(login_url="login")
def quotation_list(request):
    quotations = Quotation.objects.all().order_by("-quotation_date")

    status_filter = request.GET.get("status", "")
    if status_filter:
        quotations = quotations.filter(status=status_filter)

    return render(request, "quotations/list.html", {
        "quotations": quotations,
        "status_filter": status_filter,
    })


@login_required(login_url="login")
def quotation_add(request):
    if request.method == "POST":
        form = QuotationForm(request.POST)
        formset = QuotationItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            quotation = form.save(commit=False)
            quotation.created_by = request.user
            quotation.save()
            formset.instance = quotation
            formset.save()
            messages.success(request, "Quotation created successfully.")
            return redirect("quotation_detail", pk=quotation.pk)
    else:
        form = QuotationForm()
        formset = QuotationItemFormSet()
    return render(request, "quotations/form.html", {
        "form": form, "formset": formset, "title": "Create Quotation",
    })


@login_required(login_url="login")
def quotation_edit(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.method == "POST":
        form = QuotationForm(request.POST, instance=quotation)
        formset = QuotationItemFormSet(request.POST, instance=quotation)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Quotation updated successfully.")
            return redirect("quotation_detail", pk=quotation.pk)
    else:
        form = QuotationForm(instance=quotation)
        formset = QuotationItemFormSet(instance=quotation)
    return render(request, "quotations/form.html", {
        "form": form, "formset": formset, "title": "Edit Quotation",
    })


@login_required(login_url="login")
def quotation_delete(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    if request.method == "POST":
        quotation.delete()
        messages.success(request, "Quotation deleted.")
        return redirect("quotation_list")
    return render(request, "quotations/confirm_delete.html", {"quotation": quotation})


@login_required(login_url="login")
def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, "quotations/detail.html", {"quotation": quotation})


@login_required(login_url="login")
def quotation_pdf(request, pk):
    """Generates a downloadable PDF quotation (the 'Extra Feature' from the PDF spec)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    import io

    quotation = get_object_or_404(Quotation, pk=pk)
    styles = getSampleStyleSheet()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []

    story.append(Paragraph("SalesAI CRM - Quotation", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Quotation #: {quotation.id}", styles["Normal"]))
    story.append(Paragraph(f"Date: {quotation.quotation_date}", styles["Normal"]))
    story.append(Paragraph(f"Customer: {quotation.customer.name}", styles["Normal"]))
    if quotation.customer.company:
        story.append(Paragraph(f"Company: {quotation.customer.company}", styles["Normal"]))
    story.append(Spacer(1, 16))

    data = [["Product", "Qty", "Price", "Total"]]
    for item in quotation.items.all():
        data.append([
            item.product.name,
            str(item.quantity),
            f"Rs. {item.price}",
            f"Rs. {item.line_total()}",
        ])

    table = Table(data, colWidths=[70 * mm, 25 * mm, 35 * mm, 35 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563eb")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 16))

    story.append(Paragraph(f"Subtotal: Rs. {quotation.subtotal()}", styles["Normal"]))
    story.append(Paragraph(f"Discount: {quotation.discount}%", styles["Normal"]))
    story.append(Paragraph(f"GST: {quotation.gst}%", styles["Normal"]))
    story.append(Paragraph(f"<b>Total: Rs. {quotation.total()}</b>", styles["Normal"]))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="quotation_{quotation.id}.pdf"'
    return response
