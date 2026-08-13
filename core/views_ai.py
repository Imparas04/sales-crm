from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Lead, Customer
from .decorators import role_required
from . import ai_service


@login_required(login_url="login")
def ai_score_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        try:
            ai_service.score_lead(lead)
            messages.success(request, f"AI scored this lead: {lead.ai_score}/100")
        except ai_service.AIServiceError as e:
            messages.error(request, str(e))
        return redirect("lead_detail", pk=lead.pk)
    return render(request, "ai/confirm_score.html", {"lead": lead})


@login_required(login_url="login")
def ai_followup_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    message = None
    error = None
    if request.method == "POST":
        try:
            message = ai_service.generate_followup_message(lead=lead)
        except ai_service.AIServiceError as e:
            error = str(e)
    return render(request, "ai/followup_result.html", {"lead": lead, "message": message, "error": error})


@login_required(login_url="login")
def ai_customer_summary(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    result = None
    error = None
    if request.method == "POST":
        try:
            result = ai_service.generate_customer_summary(customer)
        except ai_service.AIServiceError as e:
            error = str(e)
    return render(request, "ai/summary_result.html", {"customer": customer, "result": result, "error": error})


@login_required(login_url="login")
@role_required("admin", "manager")
def ai_sales_report(request):
    report = None
    error = None
    if request.method == "POST":
        try:
            report = ai_service.generate_sales_report()
        except ai_service.AIServiceError as e:
            error = str(e)
    return render(request, "ai/sales_report.html", {"report": report, "error": error})
