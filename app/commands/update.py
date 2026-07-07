from app.storage.db import update_status, load_applications

VALID_STATUSES = ["Applied", "Interview", "Offer", "Rejected", "Withdrawn"]

STATUS_EMOJI = {
    "Applied": "🟡",
    "Interview": "🔵",
    "Offer": "🟢",
    "Rejected": "🔴",
    "Withdrawn": "⚪"
}

def handle_update(ack, respond, command):
    ack()
    text = command.get("text", "").strip()
    user_id = command["user_id"]

    if "," not in text:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: *Wrong format!*\nUsage: `/update Number, Status`\nExample: `/update 1, Interview`\nValid statuses: Applied, Interview, Offer, Rejected, Withdrawn"
                }
            }
        ], text="Wrong format")
        return

    parts = text.split(",", 1)

    try:
        number = int(parts[0].strip())
    except ValueError:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: First part must be a number. e.g. `/update 1, Interview`"
                }
            }
        ], text="Invalid number")
        return

    new_status = parts[1].strip().capitalize()

    if new_status not in VALID_STATUSES:
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f":warning: Invalid status. Choose from: {', '.join(VALID_STATUSES)}"
                }
            }
        ], text="Invalid status")
        return

    data = load_applications()
    apps = data.get(user_id, [])

    if not apps or number < 1 or number > len(apps):
        respond(blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":warning: Invalid number. Use `/mystatus` to see your application numbers."
                }
            }
        ], text="Invalid number")
        return

    company = apps[number - 1]["company"]
    role = apps[number - 1]["role"]
    result = update_status(user_id, number, new_status)
    emoji = STATUS_EMOJI.get(new_status, "⚪")

    respond(blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Status Updated! ✅"
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
                    "text": f"*New Status:*\n{emoji} {new_status}"
                }
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
                    "text": "Use `/mystatus` to view all your applications"
                }
            ]
        }
    ], text=result)