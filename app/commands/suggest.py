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

    try:
        apps_text = "\n".join([
            f"{i+1}. {app['company']} - {app['role']} - Status: {app['status']}"
            for i, app in enumerate(apps)
        ])

        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            f"""You are a job search coach. Give 2-3 short bullet point suggestions for this job seeker. Be direct and encouraging. Under 80 words.

Applications:
{apps_text}"""
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
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "Powered by Gemini AI"
                    }
                ]
            }
        ], text=suggestion)

    except Exception as e:
        respond(text=f"Sorry, could not get suggestions right now. Error: {str(e)}")