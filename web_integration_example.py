from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import json
import tempfile

# Import the core marketing functions from the wrapper
from marketing_wrapper import (
    run_marketing_audit,
    analyze_competitors,
    get_social_media_plan,
    build_pdf_report
)

app = FastAPI(title="AI Marketing Suite API")

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Marketing Suite API integration example."}

@app.get("/analyze")
async def analyze_url(url: str = Query(..., description="The URL of the website to analyze")):
    """
    Analyzes a webpage for marketing effectiveness.
    """
    try:
        return run_marketing_audit(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/competitor")
async def scan_competitor(url: str = Query(..., description="The URL of the competitor website")):
    """
    Scans a competitor website for positioning, pricing, and trust signals.
    """
    try:
        # Wrapper takes a list of URLs, here we just pass one
        results = analyze_competitors([url])
        return results["competitors"][0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/social-calendar")
async def get_social_calendar(
    topic: str = Query(..., description="The topic for the social media calendar"),
    platforms: Optional[str] = Query("linkedin,twitter,instagram", description="Comma-separated list of platforms"),
    days: int = Query(30, description="Number of days for the calendar")
):
    """
    Generates a structured social media content calendar.
    """
    platform_list = platforms.split(",")
    return get_social_media_plan(topic, platform_list, days)

@app.post("/generate-pdf")
async def create_pdf_report(data: dict):
    """
    Generates a professional PDF marketing report from analysis data.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        output_path = tmp.name

    try:
        build_pdf_report(data, output_path)
        return FileResponse(
            output_path,
            media_type="application/pdf",
            filename="marketing_report.pdf"
            # In production, you'd use a BackgroundTask to delete output_path after sending
        )
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting integration example server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
