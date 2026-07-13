import google.generativeai as genai
import os
from app.storage.db import load_applications

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

    apps_text = "\n".join([
        f"{i+1}. {app['company']} - {app['role']} - Status: {app['status']}"
        for i, app in enumerate(apps)
    ])

    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"""You are a job search coach. Based on these job applications, give 2-3 short, specific, actionable suggestions for what the job seeker should do next. Be concise and encouraging.

Applications:
{apps_text}

Give practical next steps in bullet points. Keep it under 100 words."""
    )

    suggestion = response.text

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
                    "text": "Powered by Gemini AI • Use `/mystatus` to view all applications"
                }
            ]
        }
    ], text=suggestion)