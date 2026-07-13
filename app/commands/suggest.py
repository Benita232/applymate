import os
import google.generativeai as genai
from app.storage.db import load_applications

def build_rule_based_suggestion(apps):
    overdue = [a for a in apps if a.get("status", "").lower() in {"interviewed", "applied", "pending"}]
    if overdue:
        top = overdue[0]
        return f"• Follow up with *{top['company']}* — don't let it go cold.\n• Update your resume for the next role.\n• Apply to 2 more jobs today to keep momentum."
    return "• Keep applying consistently — aim for 3 applications a day.\n• Tailor each cover letter to the specific role.\n• Follow up on any applications older than 7 days."

def handle_suggest(ack, respond, command):
    ack()
    user_id = command["user_id"]
    data = load_applications()
    apps = data.get(user_id, [])

    if not apps:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":mag: *No applications yet!*\nUse `/apply Company, Role` to log your first one."
                }
            }
        ], text="No applications yet")
        return

    apps_text = "\n".join(
        f"{i+1}. {app['company']} - {app['role']} - Status: {app['status']}"
        for i, app in enumerate(apps)
    )

    prompt = f"""You are a job search coach.
Give 2-3 short bullet-point suggestions.
Be direct and encouraging.
Keep it under 80 words.

Applications:
{apps_text}"""

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        suggestion = response.text.strip()
        powered_by = "Powered by Gemini AI"
    except Exception:
        suggestion = build_rule_based_suggestion(apps)
        powered_by = "Powered by ApplyMate AI"

    respond(blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "AI Job Search Suggestions 🤖"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": suggestion
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"{powered_by} • Use `/mystatus` to view all applications"
                }
            ]
        }
    ], text=suggestion)