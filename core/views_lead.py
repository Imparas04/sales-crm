from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Lead, Customer
from .forms import LeadForm
from .notifications import notify


def _can_access_lead(request, lead):
    """Admin/Manager can access any lead. Sales Executive only their assigned leads."""
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == "sales_executive":
        return lead.assigned_employee_id == request.user.id
    return True


@login_required(login_url="login")
def lead_list(request):
    leads = Lead.objects.all().order_by("-created_at")

    # Sales executives only see leads assigned to them; Admin/Manager see everything.
    profile = getattr(request.user, "profile", None)
    if profile and profile.role == "sales_executive":
        leads = leads.filter(assigned_employee=request.user)

    query = request.GET.get("q", "").strip()
    if query:
        leads = leads.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(company__icontains=query)
        )

    status_filter = request.GET.get("status", "")
    if status_filter:
        leads = leads.filter(status=status_filter)

    priority_filter = request.GET.get("priority", "")
    if priority_filter:
        leads = leads.filter(priority=priority_filter)

    return render(request, "leads/list.html", {
        "leads": leads,
        "query": query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "status_choices": Lead.STATUS_CHOICES,
    })


@login_required(login_url="login")
def lead_add(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            if lead.assigned_employee:
                notify(lead.assigned_employee, f"New lead assigned to you: {lead.name}")
            messages.success(request, "Lead added successfully.")
            return redirect("lead_list")
    else:
        form = LeadForm()
    return render(request, "leads/form.html", {"form": form, "title": "Add Lead"})


@login_required(login_url="login")
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if not _can_access_lead(request, lead):
        return render(request, "403.html", {}, status=403)
    if request.method == "POST":
        old_assignee = lead.assigned_employee
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            updated_lead = form.save()
            if updated_lead.assigned_employee and updated_lead.assigned_employee != old_assignee:
                notify(updated_lead.assigned_employee, f"Lead reassigned to you: {updated_lead.name}")
            messages.success(request, "Lead updated successfully.")
            return redirect("lead_list")
    else:
        form = LeadForm(instance=lead)
    return render(request, "leads/form.html", {"form": form, "title": "Edit Lead"})


@login_required(login_url="login")
def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if not _can_access_lead(request, lead):
        return render(request, "403.html", {}, status=403)
    if request.method == "POST":
        lead.delete()
        messages.success(request, "Lead deleted.")
        return redirect("lead_list")
    return render(request, "leads/confirm_delete.html", {"lead": lead})


@login_required(login_url="login")
def lead_view(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if not _can_access_lead(request, lead):
        return render(request, "403.html", {}, status=403)
    return render(request, "leads/detail.html", {"lead": lead})


@login_required(login_url="login")
def lead_convert_to_customer(request, pk):
    """Day 10-11 business flow: Lead -> Customer (matches the PDF's Lead -> Customer step)."""
    lead = get_object_or_404(Lead, pk=pk)
    if not _can_access_lead(request, lead):
        return render(request, "403.html", {}, status=403)
    if request.method == "POST":
        customer = Customer.objects.create(
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            company=lead.company,
            assigned_employee=lead.assigned_employee,
            status="active",
        )
        lead.status = "won"
        lead.save()
        messages.success(request, f"Lead converted to customer: {customer.name}")
        return redirect("customer_detail", pk=customer.pk)
    return render(request, "leads/confirm_convert.html", {"lead": lead})
