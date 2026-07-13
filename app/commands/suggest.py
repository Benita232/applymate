import os
import time
import google.generativeai as genai
from app.storage.db import load_applications

def build_rule_based_suggestion(apps):
    overdue = [a for a in apps if a.get("status", "").lower() in {"interviewed", "applied", "pending"}]
    if overdue:
        top = overdue[0]
        return f"• Follow up with {top['company']}.\n• Update your resume for the next role.\n• Apply to 2 more jobs today."
    return "• Keep applying consistently.\n• Tailor each application.\n• Follow up on older applications."

def handle_suggest(ack, respond, command):
    ack()
    user_id = command["user_id"]
    data = load_applications()
    apps = data.get(user_id, [])

    if not apps:
        respond(text="No applications yet. Use /apply Company, Role to log your first one.")
        return

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        respond(text=build_rule_based_suggestion(apps))
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
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        suggestion = response.text.strip()
    except Exception:
        suggestion = build_rule_based_suggestion(apps)

    respond(text=suggestion)