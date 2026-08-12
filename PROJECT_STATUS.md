# PROJECT STATUS — SalesAI CRM (Django)

## Team
- Paras: Backend | Friend: Frontend (has repo access)

## Day 1 Setup ✅ | Day 3 Schema ✅ | Day 5-6 Auth ✅ | Day 8-14 CRUD ✅ | Day 12-13 Followup+Product ✅ | Day 20-21 Quotation+Sales ✅

## Day 22-23 — Dashboard KPIs + Charts ✅
- core/views.py dashboard_view rewritten: Total Customers/Leads/Sales, Monthly Revenue,
  Conversion Rate, Pending Follow-ups — all computed live from DB
- Chart.js (via CDN) — Lead Status doughnut chart, Top Products by Revenue bar chart
- templates/dashboard.html rewritten with KPI card grid + two canvas charts

## Day 24-27 — AI Module ✅ (all 4 features from the spec)
- core/ai_service.py: wraps Google Gemini API (model: gemini-2.5-flash, FREE tier, no
  credit card - get key at aistudio.google.com/apikey) via `requests`.
  Reads AI_API_KEY from .env. Raises AIServiceError with a clear message if key missing or
  API call fails (never crashes the page — caught in views, shown as a message to the user).
  - score_lead(lead) — asks AI for JSON {score, priority, recommendation}, saves to Lead model
  - generate_followup_message(lead/customer) — plain text follow-up message
  - generate_customer_summary(customer) — JSON {summary, purchase_probability, recommended_action}
    based on actual purchase history pulled from Sale/SaleItem
  - generate_sales_report() — aggregates this month's real sales/lead data, asks AI to summarize
  - Every AI call is logged to the AILog model (feature, input, output, timestamp)
- core/views_ai.py: 4 views wired to the above. ai_sales_report restricted to admin/manager via
  @role_required (first real use of that decorator, built back on Day 5-6)
- templates/ai/: confirm_score, followup_result, summary_result, sales_report
- Buttons added to lead detail ("AI Score This Lead", "AI Follow-up Message") and customer detail
  ("AI Customer Summary")
- requirements.txt: added requests==2.32.3

TESTED with a mocked AI call (no real API key used) — confirmed: lead score saves correctly to
DB, followup message renders, customer summary renders with real purchase data, sales_executive
role is blocked from the sales report (302 redirect) while admin role can access it (200 + report
shown), and all 4 calls create an AILog row. Real API calls need an actual AI_API_KEY in .env —
untested against the live Anthropic API since that requires your own key with credits.

## Day 28-30 — (next: final testing, deployment, docs, presentation)


## Note: switched AI provider Anthropic -> Google Gemini (free tier, no card needed for students).
_extract_json() handles Gemini's habit of wrapping JSON responses in ```json fences.
