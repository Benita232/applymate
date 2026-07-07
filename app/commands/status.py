from app.storage.db import get_applications, load_applications

STATUS_EMOJI = {
    "Applied": "🟡",
    "Interview": "🔵",
    "Offer": "🟢",
    "Rejected": "🔴",
    "Withdrawn": "⚪"
}

def handle_status(ack, respond, command):
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

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Your Applications ({len(apps)}) 📋"
            }
        },
        {"type": "divider"}
    ]

    for i, app in enumerate(apps, 1):
        emoji = STATUS_EMOJI.get(app["status"], "⚪")
        blocks.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{i}. {app['company']}*\n{app['role']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Status:*\n{emoji} {app['status']}"
                }
            ]
        })

    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "Use `/update Number, Status` to update • Statuses: Applied, Interview, Offer, Rejected, Withdrawn"
            }
        ]
    })

    respond(blocks=blocks, text="Your applications")