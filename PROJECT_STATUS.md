# PROJECT STATUS — SalesAI CRM (Django)

## Team
- Paras: Backend (Django, MySQL, Auth, Business logic, AI)
- Friend: Frontend (HTML/CSS/JS, Dashboard UI) — not started yet, friend on leave

## Day 1 — Project Setup ✅
- Django project + core app created
- settings.py: env vars via python-dotenv, MySQL via PyMySQL
- MySQL root password reset (MySQL80 service), sales_crm DB created
- Verified: migrate + runserver working, /ping-db/ confirms DB connection

## Day 3 — Database Schema (models.py) ✅
11 models created in core/models.py:
- UserProfile (extends Django User; role = admin/manager/sales_executive)
- Customer
- Lead (includes ai_score + ai_recommendation fields for Day 25 AI feature)
- FollowUp (linked to customer or lead)
- Product
- Quotation + QuotationItem (with subtotal/total calculation incl. discount + GST)
- Sale + SaleItem (same calculation logic, invoice-based)
- Notification
- AILog (stores every AI feature call for audit/history)
All registered in core/admin.py with list_display/filters/search — usable via Django admin panel immediately.
Validated: `makemigrations --dry-run` runs clean, no field/relation errors.

## Day 4 — (next)
- Run actual `python manage.py makemigrations` + `migrate` on your MySQL DB
- Create a superuser, explore Django admin panel with the new models
- ER diagram from these relationships (for the SRS/documentation deliverable)
