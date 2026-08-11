# PROJECT STATUS — SalesAI CRM (Django)

## Team
- Paras: Backend (Django, MySQL, Auth, Business logic, AI)
- Friend: Frontend (HTML/CSS/JS, Dashboard UI) — not started yet, friend on leave

## Day 1 — Project Setup ✅
- Django project + core app, MySQL via PyMySQL, .env config
- MySQL root password reset, sales_crm DB created, verified working

## Day 3 — Database Schema (models.py) ✅
- 11 models: UserProfile, Customer, Lead, FollowUp, Product, Quotation+Items, Sale+Items, Notification, AILog
- Registered in Django admin with list_display/filters/search

## Day 5-6 — Authentication ✅
- core/forms.py: RegisterForm (validates password match, unique username/email), LoginForm
- core/views.py: register_view, login_view, logout_view, dashboard_view
  - Password hashing handled automatically by Django's User.objects.create_user() (PBKDF2)
  - Session management handled automatically by Django's login()/logout() (session cookie + DB-backed sessions)
  - Already-logged-in users get redirected away from login/register pages
- core/decorators.py: role_required() decorator for restricting views by role (admin/manager/sales_executive) — not wired into any view yet, ready for Day 8 (user roles)
- templates/login.html, register.html, dashboard.html — functional but plain, friend will style
- Tested end-to-end (register -> login -> access dashboard -> logout, plus wrong password and duplicate username rejected correctly) against an in-memory test DB — all passed

## Day 8 — (next)
- Wire role_required() into views that need role restriction
- Decide which pages Admin/Manager/Sales Executive each see differently
