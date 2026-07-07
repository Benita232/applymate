from app.storage.db import update_status

VALID_STATUSES = ["Applied", "Interview", "Offer", "Rejected", "Withdrawn"]

def handle_update(ack, respond, command):
    ack()
    text = command.get("text", "").strip()
    user_id = command["user_id"]

    if "," not in text:
        respond("Usage: `/update Number, Status` — e.g. `/update 1, Interview`\nValid statuses: Applied, Interview, Offer, Rejected, Withdrawn")
        return

    parts = text.split(",", 1)
    
    try:
        number = int(parts[0].strip())
    except ValueError:
        respond("First part must be a number. e.g. `/update 1, Interview`")
        return

    new_status = parts[1].strip().capitalize()

    if new_status not in VALID_STATUSES:
        respond(f"Invalid status. Choose from: {', '.join(VALID_STATUSES)}")
        return

    result = update_status(user_id, number, new_status)
    respond(result)