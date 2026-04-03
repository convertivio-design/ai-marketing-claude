"""
AI Marketing Suite - Core Functions Wrapper
A utility module that simplifies integrating the suite's functionality
into any Python web application (FastAPI, Flask, Django, etc.).
"""

import os
from scripts.analyze_page import analyze as analyze_page_func
from scripts.competitor_scanner import scan_competitor as scan_competitor_func
from scripts.social_calendar import generate_calendar as generate_calendar_func

def run_marketing_audit(url: str):
    """
    Run a full marketing audit for a URL.
    Returns a dict with scores, SEO analysis, trust signals, and more.
    """
    if not url.startswith("http"):
        url = "https://" + url

    # Analyze the page
    results = analyze_page_func(url)

    # Handle errors if necessary
    if results.get("status") == "error":
        raise Exception(f"Audit failed: {results.get('message')}")

    return results

def analyze_competitors(urls: list):
    """
    Scan multiple competitor URLs and return their positioning data.
    """
    competitors = []
    for url in urls:
        if not url.startswith("http"):
            url = "https://" + url
        competitors.append(scan_competitor_func(url))

    return {"competitors": competitors}

def get_social_media_plan(topic: str, platforms: list = None, days: int = 30):
    """
    Generate a content calendar for a given topic and platforms.
    """
    if platforms is None:
        platforms = ["linkedin", "twitter", "instagram"]

    return generate_calendar_func(topic, platforms, days)

def build_pdf_report(analysis_data: dict, output_filename: str = "report.pdf"):
    """
    Create a professional PDF report from analysis results.
    """
    # Import here to avoid dependency error if reportlab is not installed
    try:
        from scripts.generate_pdf_report import generate_report as generate_report_func
        generate_report_func(analysis_data, output_filename)
        return os.path.abspath(output_filename)
    except ImportError:
        raise Exception("PDF Generation failed: reportlab is required. Install with 'pip install reportlab'")
    except Exception as e:
        raise Exception(f"PDF Generation failed: {str(e)}")

# --- Usage Example ---
if __name__ == "__main__":
    # 1. Audit a site
    print("Auditing example.com...")
    audit_results = run_marketing_audit("https://example.com")
    print(f"Overall Score: {audit_results['analysis']['overall_score']}")

    # 2. Get a social plan
    print("Generating 7-day plan for 'AI Consulting'...")
    plan = get_social_media_plan("AI Consulting", days=7)
    print(f"Total days generated: {len(plan['calendar'])}")
