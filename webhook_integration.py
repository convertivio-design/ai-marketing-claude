import requests
import json
import os
from marketing_wrapper import run_marketing_audit

def send_to_webhook(webhook_url: str, message_payload: dict):
    """
    General purpose function to send JSON payload to a webhook.
    """
    try:
        response = requests.post(
            webhook_url,
            data=json.dumps(message_payload),
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        print(f"Successfully sent update to webhook.")
    except Exception as e:
        print(f"Failed to send update to webhook: {e}")

def format_discord_payload(analysis: dict):
    """
    Format marketing audit results for a Discord webhook using embeds.
    """
    score = int(analysis['overall_score'] * 10)
    color = 0x00ff00 if score >= 75 else 0xffff00 if score >= 50 else 0xff0000

    embed = {
        "title": f"🚀 Marketing Audit: {analysis['url']}",
        "description": f"New audit completed for **{analysis['url']}**.",
        "color": color,
        "fields": [
            {"name": "Overall Score", "value": f"**{score}/100**", "inline": True},
            {"name": "SEO Score", "value": f"{analysis['analysis']['scores']['seo']}/10", "inline": True},
            {"name": "CTA Score", "value": f"{analysis['analysis']['scores']['cta']}/10", "inline": True},
        ],
        "footer": {"text": "AI Marketing Suite - Webhook Integration"}
    }

    # Add key findings
    findings = analysis['analysis']['seo']['heading_issues'][:3]
    if findings:
        embed["fields"].append({"name": "Top Issues", "value": "\n".join([f"• {f}" for f in findings])})

    return {"embeds": [embed]}

def format_slack_payload(analysis: dict):
    """
    Format marketing audit results for a Slack webhook using Block Kit.
    """
    score = int(analysis['overall_score'] * 10)

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🚀 New Marketing Audit Complete"}
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*URL:* {analysis['url']}\n*Overall Score:* `{score}/100`"}
        },
        {"type": "divider"}
    ]

    # Add score breakdown
    breakdown_text = ""
    for cat, val in analysis['analysis']['scores'].items():
        breakdown_text += f"• *{cat.capitalize()}:* `{val}/10` \n"

    blocks.append({
        "type": "section",
        "text": {"type": "mrkdwn", "text": breakdown_text}
    })

    return {"blocks": blocks}

def audit_and_notify(url: str, webhook_url: str, platform: str = "discord"):
    """
    Run audit and send a notification automatically.
    """
    print(f"Auditing {url}...")
    results = run_marketing_audit(url)

    if platform.lower() == "discord":
        payload = format_discord_payload(results)
    elif platform.lower() == "slack":
        payload = format_slack_payload(results)
    else:
        # Default simple payload
        payload = {"text": f"Audit complete for {url}. Overall score: {results['overall_score']}"}

    send_to_webhook(webhook_url, payload)

if __name__ == "__main__":
    # To test, replace with your actual webhook URL and run:
    # python3 webhook_integration.py
    TEST_WEBHOOK = "https://discord.com/api/webhooks/..."
    # audit_and_notify("https://example.com", TEST_WEBHOOK, "discord")
    print("Example ready. Uncomment the line above and provide a webhook URL to test.")
