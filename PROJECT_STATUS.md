# PROJECT STATUS — SalesAI CRM (Django)

## Team
- Paras: Backend (Django, MySQL, Auth, Business logic, AI)
- Friend: Frontend (HTML/CSS/JS, Dashboard UI)

## Day 1 — Project Setup ✅
- `django-admin startproject sales_crm` + `core` app created
- settings.py: env vars via python-dotenv, MySQL via PyMySQL (Windows-friendly, avoids mysqlclient build issues)
- templates/ and static/ wired up at project level (not app level) so friend has one clear folder to work in
- core/views.py: home view (renders login.html) + ping-db view (tests MySQL connection)
- core/urls.py + sales_crm/urls.py wired
- Placeholder login.html + style.css
- .env.example, .gitignore, README, this status file
- git repo initialized, Day 1 pushed

## Day 2 — (next)
- MySQL: create `sales_crm` database
- Discuss ER diagram before writing models.py (Day 3)
- Friend starts on static HTML for dashboard/login/customer pages (design only, no logic yet)
