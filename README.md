# SalesAI CRM

**AI-Powered Sales & Customer Management Platform**

A full-stack web application built for a simulated client engagement (ABC Sales & Services Pvt. Ltd.) as a 1-month internship project. It replaces manual, spreadsheet-based sales tracking with a role-aware CRM that covers the entire sales lifecycle — lead capture, follow-ups, quotations, sales — with AI-driven insights layered on top.

> Manage Customers. Convert Leads. Automate Follow-ups. Grow Sales with AI.

---

## ✨ Features

- **Authentication & Roles** — Admin, Manager, and Sales Executive roles with backend-enforced permissions (not just hidden menus — direct URL access to a restricted page returns a real 403).
- **Customer Management** — Add, edit, delete, search, and filter customers.
- **Lead Management** — Full lead pipeline (`New → Contacted → Qualified → Proposal Sent → Negotiation → Won/Lost`), one-click conversion to Customer. Sales Executives see only their own assigned leads.
- **Product Management** — Restricted to Admin/Manager.
- **Follow-up Scheduling** — Linked to a Customer or a Lead, with a Today's / Overdue / Upcoming / Completed dashboard.
- **Quotations & Sales** — Multi-item quotations with automatic discount and GST calculation, downloadable PDF invoices, and one-click quotation-to-sale conversion with auto-generated invoice numbers.
- **Dashboard** — Live KPIs (customers, leads, sales, revenue, conversion rate, pending follow-ups) and Chart.js visualizations.
- **AI Module** (powered by the Groq API):
  - 🎯 **Lead Scoring** — 0–100 score, priority, and a recommendation
  - ✉️ **AI Follow-up Message Generator**
  - 📊 **Customer Summary** — purchase history summary + purchase probability
  - 📈 **AI Sales Report** — monthly performance summary (Admin/Manager only)
  - Every AI call is logged for auditing.
- **Notifications** — Auto-triggered on lead assignment, follow-up scheduling, and sales.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5 |
| Database | MySQL 8 (via PyMySQL) |
| Frontend | HTML5, CSS3, JavaScript, Chart.js |
| AI | Groq API (OpenAI-compatible) |
| PDF Generation | ReportLab |
| Version Control | Git & GitHub |

---

## 🚀 Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/imparas04/sales-crm.git
   cd sales-crm
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL**
   ```sql
   CREATE DATABASE sales_crm;
   ```

5. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in your values:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=sales_crm
   DB_USER=root
   DB_PASSWORD=your-mysql-password
   DB_HOST=localhost
   DB_PORT=3306
   AI_API_KEY=your-groq-api-key
   ```
   Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys).

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create a superuser (optional, for Django Admin access)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/`.

---

## 👥 Roles & Permissions

| Feature | Sales Executive | Admin / Manager |
|---|---|---|
| Customers | Full access | Full access |
| Leads | Only own assigned leads | All leads |
| Products | View only | Full access |
| Follow-ups / Quotations / Sales | Full access | Full access |
| AI Sales Report | No access | Full access |

---

## 📁 Project Structure

```
sales_crm/
├── manage.py
├── requirements.txt
├── .env.example
├── sales_crm/          # Project settings, URLs
├── core/                # Models, views, forms, AI service, decorators
│   ├── models.py
│   ├── views*.py         # Split by module (customer, lead, product, followup, quotation, sale, ai, notification)
│   ├── ai_service.py
│   ├── decorators.py
│   └── urls.py
├── templates/            # HTML templates, organized by module
├── static/css/           # Stylesheet
└── docs/                 # Project documentation (see below)
```

---

## 📄 Documentation

Full project documentation is in the `docs/` folder:

- Software Requirements Specification (SRS)
- ER Diagram
- Database Schema Document
- UI Wireframes
- API Documentation
- Test Cases
- Bug Report
- User Manual
- Final Project Report

---

## 👨‍💻 Team

- **Backend:** Paras Choudhary — Django, MySQL, business logic, AI integration, security
- **Frontend:** Irfan Mulla — HTML/CSS/JS, UI design

---

## 📌 Notes

- This is an internship project built to simulate a real client engagement, not a production deployment.
- The AI Module requires an active internet connection and a valid `AI_API_KEY`.