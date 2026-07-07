from app.storage.db import add_application

def handle_apply(ack, respond, command):
    ack()
    text = command.get("text", "").strip()
    user_id = command["user_id"]

    if "," not in text:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: *Wrong format!*\nUsage: `/apply Company, Role`\nExample: `/apply Google, Software Engineer`"
                }
            }
        ], text="Wrong format")
        return

    parts = text.split(",", 1)
    company = parts[0].strip()
    role = parts[1].strip()

    if not company or not role:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: Please provide both a company and a role."
                }
            }
        ], text="Missing fields")
        return

    result = add_application(user_id, company, role)

    if "already applied" in result:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":repeat: {result}"
                }
            }
        ], text=result)
        return

    respond(blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Application Logged! :briefcase:"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Company:*\n{company}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Role:*\n{role}"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Status:*\n🟡 Applied"
                },
            ]
        },
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Use `/mystatus` to view all applications • `/update Number, Status` to update"
                }
            ]
        }
    ], text=result)