from app.storage.db import get_applications

def handle_status(ack, respond, command):
    ack()
    user_id = command["user_id"]
    result = get_applications(user_id)
    respond(result)