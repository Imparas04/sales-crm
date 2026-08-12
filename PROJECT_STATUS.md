# PROJECT STATUS — SalesAI CRM (Django)

## Team
- Paras: Backend | Friend: Frontend (~15% done, `frontend` branch)

## Day 1-28 all complete: Setup, Schema, Auth, CRUD (Customer/Lead/Product/Followup),
## Quotation+Sales+PDF, Dashboard KPIs+Charts, AI Module (Groq), Notifications

## Day 8 (revisited) — Proper Role-Based Access Control ✅
Previously only AI Sales Report was role-restricted. Now:
- core/decorators.py: role_required() now returns a REAL 403 Forbidden page (templates/403.html)
  instead of a silent redirect - direct URL access by an unauthorized role is blocked with a
  clear error, not just hidden from the menu.
- core/views_product.py: product_add/edit/delete restricted to admin/manager via @role_required.
  product_list stays open to everyone (sales executives need to browse products to build quotations).
- core/views_lead.py:
  - lead_list: sales_executive sees ONLY leads assigned to them; admin/manager see all leads
    (matches the PDF spec: "Sales Executive -> View assigned leads" vs "Admin -> Manage leads")
  - Added _can_access_lead() ownership check, applied to lead_detail/edit/delete/convert -
    a sales_executive typing another lead's URL directly gets 403, not the data
- templates/dashboard.html: nav links now conditional on profile.role (AI Sales Report hidden
  for sales_executive)
- templates/products/list.html: "Add Product" button and per-row Edit/Delete links hidden for
  sales_executive

Tested extensively: cross-user lead access blocked (view/edit/convert all return 403), product
management blocked for sales_executive (both GET and POST), admin retains full access, dashboard
and product list correctly hide restricted UI per role, 403 page renders without crashing.

## Still remaining (non-coding):
- Manual click-through testing, Documentation (SRS/ER/API docs/User Manual/Report), Deployment
- Friend's frontend styling
