from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    """Restrict a view to users whose profile.role is in allowed_roles.
    Usage: @role_required("admin", "manager")
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            profile = getattr(request.user, "profile", None)
            if profile is None or profile.role not in allowed_roles:
                messages.error(request, "You don't have permission to access this page.")
                return redirect("dashboard")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
