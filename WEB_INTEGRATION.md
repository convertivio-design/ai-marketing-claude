# Integrating AI Marketing Suite into a Web App

This guide explains how to integrate the marketing analysis and automation tools into your own web application.

## 1. Core Integration Layer (`marketing_wrapper.py`)

We've provided a `marketing_wrapper.py` file that simplifies the usage of the existing Python scripts. Instead of calling scripts via the command line, you can import these high-level functions directly into your backend code:

- `run_marketing_audit(url)`: Performs a full SEO and conversion analysis on a webpage.
- `analyze_competitors(urls)`: Scans multiple competitor sites for positioning and pricing.
- `get_social_media_plan(topic, platforms, days)`: Generates a 30-day (or custom duration) content calendar.
- `build_pdf_report(analysis_data, output_filename)`: Creates a professional PDF report.

## 2. Web API Example (`web_integration_example.py`)

The provided `web_integration_example.py` demonstrates how to build a REST API using **FastAPI** that exposes these marketing tools.

### Prerequisites

You'll need a few Python packages:
```bash
pip install fastapi uvicorn
pip install -r requirements.txt
pip install reportlab  # Optional: For PDF reports
```

### Running the Example API

```bash
python3 web_integration_example.py
```

Once running, you can access the interactive documentation at `http://localhost:8000/docs` to test the following endpoints:

- `GET /analyze?url=example.com`: Get marketing analysis JSON data.
- `GET /competitor?url=competitor.com`: Get competitor insights.
- `GET /social-calendar?topic=YourTopic&days=30`: Get a content calendar.
- `POST /generate-pdf`: Send analysis JSON and receive a professional PDF file.

## 3. Recommended Workflow

For a production-grade web app, we recommend:

1. **Background Tasks**: Marketing audits and competitor scans can take 10-15 seconds. Use background tasks (like FastAPI's `BackgroundTasks` or Celery) so your users don't wait for a response.
2. **Caching**: Store analysis results in a database (e.g., PostgreSQL or Redis) to avoid re-scanning the same URL multiple times.
3. **Frontend Integration**: Use a framework like React, Vue, or Next.js to display the JSON results in a beautiful dashboard. The `overall_score` can be shown using a gauge component, and the `findings` list can be displayed as actionable tasks.

## 4. Key Functions to Use

### Marketing Audit
```python
from marketing_wrapper import run_marketing_audit

results = run_marketing_audit("https://your-client-site.com")
score = results['analysis']['overall_score']
findings = results['analysis']['seo']['heading_issues']
```

### Social Media Plan
```python
from marketing_wrapper import get_social_media_plan

plan = get_social_media_plan("SaaS Marketing", platforms=["linkedin", "twitter"], days=14)
for day in plan['calendar']:
    print(f"Day {day['day']}: {day['topic_angle']}")
```

### PDF Generation
```python
from marketing_wrapper import build_pdf_report

# 'data' should be the JSON returned by run_marketing_audit
pdf_path = build_pdf_report(data, "client_report.pdf")
```
