from app.storage.db import delete_application

def handle_delete(ack, respond, command):
    ack()
    text = command.get("text", "").strip()
    user_id = command["user_id"]

    try:
        number = int(text)
    except ValueError:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: *Wrong format!*\nUsage: `/delete Number`\nExample: `/delete 1`"
                }
            }
        ], text="Wrong format")
        return

    removed, error = delete_application(user_id, number)

    if error:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning: {error}"
                }
            }
        ], text=error)
        return

    respond(blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Application Deleted 🗑️"
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Company:*\n{removed['company']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Role:*\n{removed['role']}"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "Use `/mystatus` to view remaining applications"
                }
            ]
        }
    ], text=f"Deleted {removed['company']}")