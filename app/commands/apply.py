from app.storage.db import add_application

def handle_apply(ack, say, command):
    ack()
    text = command.get("text", "").strip()
    user_id = command["user_id"]

    if "," not in text:
        say("Usage: `/apply Company, Role` — e.g. `/apply Google, Software Engineer`")
        return

    parts = text.split(",", 1)
    company = parts[0].strip()
    role = parts[1].strip()

    if not company or not role:
        say("Please provide both a company and a role. e.g. `/apply Google, Software Engineer`")
        return

    result = add_application(user_id, company, role)
    say(result)