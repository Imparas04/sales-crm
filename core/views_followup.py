from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import FollowUp
from .forms import FollowUpForm
from .notifications import notify


@login_required(login_url="login")
def followup_dashboard(request):
    """Matches the PDF's Follow-up dashboard: Today's / Upcoming / Overdue / Completed."""
    today = timezone.localdate()

    todays = FollowUp.objects.filter(date=today, status="pending")
    upcoming = FollowUp.objects.filter(date__gt=today, status="pending").order_by("date", "time")
    overdue = FollowUp.objects.filter(date__lt=today, status="pending").order_by("date", "time")
    completed = FollowUp.objects.filter(status="completed").order_by("-date")[:20]

    return render(request, "followups/dashboard.html", {
        "todays": todays,
        "upcoming": upcoming,
        "overdue": overdue,
        "completed": completed,
    })


@login_required(login_url="login")
def followup_list(request):
    followups = FollowUp.objects.all().order_by("-date", "-time")

    status_filter = request.GET.get("status", "")
    if status_filter:
        followups = followups.filter(status=status_filter)

    type_filter = request.GET.get("type", "")
    if type_filter:
        followups = followups.filter(type=type_filter)

    return render(request, "followups/list.html", {
        "followups": followups,
        "status_filter": status_filter,
        "type_filter": type_filter,
    })


@login_required(login_url="login")
def followup_add(request):
    if request.method == "POST":
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save()
            if followup.assigned_employee:
                notify(followup.assigned_employee, f"Follow-up scheduled: {followup.contact_name} on {followup.date}")
            messages.success(request, "Follow-up scheduled successfully.")
            return redirect("followup_list")
    else:
        form = FollowUpForm()
    return render(request, "followups/form.html", {"form": form, "title": "Schedule Follow-up"})


@login_required(login_url="login")
def followup_edit(request, pk):
    followup = get_object_or_404(FollowUp, pk=pk)
    if request.method == "POST":
        form = FollowUpForm(request.POST, instance=followup)
        if form.is_valid():
            form.save()
            messages.success(request, "Follow-up updated successfully.")
            return redirect("followup_list")
    else:
        form = FollowUpForm(instance=followup)
    return render(request, "followups/form.html", {"form": form, "title": "Edit Follow-up"})


@login_required(login_url="login")
def followup_delete(request, pk):
    followup = get_object_or_404(FollowUp, pk=pk)
    if request.method == "POST":
        followup.delete()
        messages.success(request, "Follow-up deleted.")
        return redirect("followup_list")
    return render(request, "followups/confirm_delete.html", {"followup": followup})


@login_required(login_url="login")
def followup_mark_complete(request, pk):
    followup = get_object_or_404(FollowUp, pk=pk)
    if request.method == "POST":
        followup.status = "completed"
        followup.save()
        messages.success(request, "Follow-up marked as completed.")
        return redirect("followup_dashboard")
    return render(request, "followups/confirm_complete.html", {"followup": followup})
