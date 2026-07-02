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
def apply_command(ack, say, command):
    handle_apply(ack, say, command)

@app.command("/status")
def status_command(ack, say, command):
    handle_status(ack, say, command)

@app.command("/update")
def update_command(ack, say, command):
    handle_update(ack, say, command)

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(port=3000)