import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

from app.commands.apply import handle_apply
from app.commands.status import handle_status
from app.commands.update import handle_update

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.command("/apply")
def apply_command(ack, respond, command):
    handle_apply(ack, respond, command)

@app.command("/mystatus")
def status_command(ack, respond, command):
    handle_status(ack, respond, command)

@app.command("/update")
def update_command(ack, respond, command):
    handle_update(ack, respond, command)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=3000, debug=True)