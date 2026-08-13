from functools import wraps
from django.shortcuts import redirect, render


def role_required(*allowed_roles):
    """Restrict a view to users whose profile.role is in allowed_roles.
    Usage: @role_required("admin", "manager")
    Unauthenticated users get redirected to login. Authenticated users without
    permission get a real 403 Forbidden page (not a silent redirect) - so
    someone typing the URL directly, or a link that slips through, is blocked
    with a clear error rather than being bounced somewhere unexpected.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")
            profile = getattr(request.user, "profile", None)
            if profile is None or profile.role not in allowed_roles:
                return render(request, "403.html", {}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
