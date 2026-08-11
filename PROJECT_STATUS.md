# PROJECT STATUS — SalesAI CRM (Django)

## Team
- Paras: Backend (Django, MySQL, Auth, Business logic, AI)
- Friend: Frontend (HTML/CSS/JS, Dashboard UI) — not started yet

## Day 1 — Setup ✅ | Day 3 — Schema (11 models) ✅ | Day 5-6 — Auth ✅

## Day 8-14 — Customer + Lead CRUD ✅
- core/forms.py: added CustomerForm, LeadForm (ModelForm-based)
- core/views_customer.py: list (with search q= + filter status=), add, edit, delete, detail
- core/views_lead.py: list (search + filter status/priority), add, edit, delete, detail,
  + lead_convert_to_customer (Lead -> Customer flow per the PDF's business flow diagram; marks lead as "won")
- templates/customers/ and templates/leads/: list, form, detail, confirm_delete (+ confirm_convert for leads)
- Dashboard now links to Customers and Leads
- Tested end-to-end (add/edit/delete/search/filter/convert, all against an in-memory test DB) — all passed

## Day 15-21 — (next, this is frontend-heavy — good place to loop friend back in)
- Follow-up module (Day 12 in original plan — pull forward or keep sequence, your call)
- Product module
- Proper HTML/CSS layout + dashboard KPIs (friend's territory)
