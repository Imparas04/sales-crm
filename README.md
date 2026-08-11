# SalesAI CRM
AI-Powered Sales & Customer Management Platform (Django)

## Stack
Django + MySQL (PyMySQL) + HTML/CSS/JS + AI API

## Setup (Windows)
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`, fill DB_USER/DB_PASSWORD (create a MySQL DB named `sales_crm` first)
5. `python manage.py migrate`
6. `python manage.py runserver`
7. Visit http://127.0.0.1:8000/ and http://127.0.0.1:8000/ping-db/ to test DB connection

## Team
- Paras: backend (`core/models.py`, `core/views.py`, `core/urls.py`, `sales_crm/settings.py`)
- Friend: frontend (`templates/`, `static/`)
