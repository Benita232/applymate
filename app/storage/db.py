import json
import os

DB_FILE = "applications.json"

def load_applications():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_applications(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_application(user_id, company, role):
    data = load_applications()
    if user_id not in data:
        data[user_id] = []
    data[user_id].append({
        "company": company,
        "role": role,
        "status": "Applied",
    })
    save_applications(data)
    return f"Logged: *{role}* at *{company}* — Status: Applied"

def get_applications(user_id):
    data = load_applications()
    apps = data.get(user_id, [])
    if not apps:
        return "You have no applications logged yet. Use `/apply Company, Role` to add one."
    lines = ["*Your Applications:*"]
    for i, app in enumerate(apps, 1):
        lines.append(f"{i}. *{app['company']}* — {app['role']} | Status: {app['status']}")
    return "\n".join(lines)

def update_status(user_id, number, new_status):
    data = load_applications()
    apps = data.get(user_id, [])
    if not apps:
        return "No applications found. Use `/apply Company, Role` first."
    if number < 1 or number > len(apps):
        return f"Invalid number. You have {len(apps)} application(s)."
    apps[number - 1]["status"] = new_status
    data[user_id] = apps
    save_applications(data)
    company = apps[number - 1]["company"]
    return f"Updated *{company}* status to *{new_status}*"