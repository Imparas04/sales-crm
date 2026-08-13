"""Helper to create notifications from anywhere in the app (called from views/signals)."""
from .models import Notification


def notify(user, message):
    """Create a notification for a user. Safe no-op if user is None (e.g. unassigned lead)."""
    if user is None:
        return
    Notification.objects.create(user=user, message=message)
