"""
AI features for SalesAI CRM: Lead Scoring, Follow-up Message Generator,
Customer Summary, and Sales Report - built on Groq API (FREE tier, no credit
card required - get a key at https://console.groq.com/keys).

Note: we originally used Google Gemini, but Google's new "AQ." API key format
(rolled out mid-2026) currently breaks the plain REST endpoint for many users.
Groq uses a standard Bearer-token API key (like OpenAI) with no such issue.
"""
import json
import requests
from django.conf import settings

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"


class AIServiceError(Exception):
    """Raised when the AI API call fails or the key is missing."""
    pass


def _call_ai(prompt, max_tokens=500):
    if not settings.AI_API_KEY:
        raise AIServiceError("AI_API_KEY is not set in .env — get a free key at https://console.groq.com/keys")

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {settings.AI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL,
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise AIServiceError(f"AI API request failed: {e}")

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise AIServiceError(f"AI returned an unexpected response: {str(data)[:200]}")


def _extract_json(raw):
    """Models sometimes wrap JSON in ```json ... ``` fences - strip those before parsing."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned.strip())


def score_lead(lead):
    """Feature 1: Lead Scoring. Returns (score, priority, recommendation) and saves to lead."""
    prompt = f"""You are a sales assistant. Score this lead's likelihood to convert, from 0-100.

Lead details:
- Name: {lead.name}
- Company: {lead.company or "N/A"}
- Source: {lead.source or "N/A"}
- Budget: {lead.budget or "N/A"}
- Status: {lead.status}
- Notes: {lead.notes or "N/A"}

Respond with ONLY valid JSON, no other text, in this exact format:
{{"score": <integer 0-100>, "priority": "<LOW|MEDIUM|HIGH>", "recommendation": "<one short actionable sentence>"}}"""

    raw = _call_ai(prompt, max_tokens=200)
    try:
        result = _extract_json(raw)
    except json.JSONDecodeError:
        raise AIServiceError(f"AI returned unexpected format: {raw[:200]}")

    lead.ai_score = result.get("score")
    lead.ai_recommendation = result.get("recommendation", "")
    lead.save()

    from .models import AILog
    AILog.objects.create(
        feature="lead_scoring",
        related_lead=lead,
        input_summary=f"{lead.name} / {lead.company} / budget {lead.budget}",
        ai_output=raw,
    )
    return result


def generate_followup_message(lead=None, customer=None):
    """Feature 2: AI Follow-up Generator. Works for a Lead or a Customer."""
    target = lead or customer
    if target is None:
        raise ValueError("Provide either a lead or a customer")

    name = target.name
    interest = getattr(target, "interested_product", None) or getattr(target, "company", "") or "our services"

    prompt = f"""Write a short, warm, professional follow-up message (3-4 sentences) to a
sales lead/customer named {name} who showed interest in {interest}.
Sign off as "ABC Sales Team". Return ONLY the message text, no preamble."""

    message = _call_ai(prompt, max_tokens=250)

    from .models import AILog
    AILog.objects.create(
        feature="followup_generator",
        related_lead=lead,
        related_customer=customer,
        input_summary=f"{name} / {interest}",
        ai_output=message,
    )
    return message.strip()


def generate_customer_summary(customer):
    """Feature 3: Customer Summary — purchase history + AI-estimated purchase probability."""
    sales = customer.sales.all()
    purchase_count = sales.count()
    products = set()
    for sale in sales:
        for item in sale.items.all():
            products.add(item.product.name)

    prompt = f"""Summarize this customer for a sales rep, and estimate their probability (0-100%)
of making another purchase soon, with one recommended next action.

Customer: {customer.name}
Company: {customer.company or "N/A"}
Previous purchases: {purchase_count}
Products bought: {", ".join(products) or "None yet"}
Status: {customer.status}

Respond with ONLY valid JSON in this format:
{{"summary": "<2 sentence summary>", "purchase_probability": <integer 0-100>, "recommended_action": "<one sentence>"}}"""

    raw = _call_ai(prompt, max_tokens=300)
    try:
        result = _extract_json(raw)
    except json.JSONDecodeError:
        raise AIServiceError(f"AI returned unexpected format: {raw[:200]}")

    from .models import AILog
    AILog.objects.create(
        feature="customer_summary",
        related_customer=customer,
        input_summary=f"{customer.name}, {purchase_count} purchases",
        ai_output=raw,
    )
    return result


def generate_sales_report():
    """Feature 4: AI Sales Report — aggregate recent performance and ask for a written summary."""
    from django.utils import timezone
    from .models import Sale, Lead

    today = timezone.localdate()
    month_start = today.replace(day=1)

    this_month_sales = Sale.objects.filter(sale_date__gte=month_start)
    total_revenue = sum((s.total() for s in this_month_sales), 0)

    qualified_leads = Lead.objects.filter(status="qualified").count()
    won_leads = Lead.objects.filter(status="won").count()
    lost_leads = Lead.objects.filter(status="lost").count()

    prompt = f"""You are a sales manager's assistant. Write a short sales performance summary
(4-5 sentences) based on this data:

- This month's sales count: {this_month_sales.count()}
- This month's revenue: Rs. {total_revenue}
- Qualified leads (not yet closed): {qualified_leads}
- Won leads: {won_leads}
- Lost leads: {lost_leads}

Include one observation and one recommendation. Return ONLY the report text, no preamble."""

    report_text = _call_ai(prompt, max_tokens=400)

    from .models import AILog
    AILog.objects.create(
        feature="sales_report",
        input_summary=f"revenue={total_revenue}, qualified={qualified_leads}, won={won_leads}, lost={lost_leads}",
        ai_output=report_text,
    )
    return report_text.strip()
