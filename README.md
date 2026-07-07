# applymate
A Slack agent that tracks job applications

# ApplyMate 🎯

> Your job search co-pilot inside Slack.

ApplyMate is a Slack agent that helps job seekers track every application without leaving Slack. Log applications, check your progress, and update statuses using simple slash commands.

Built for the **Devpost Slack Agent Builder Challenge 2026**.

---

## What it does

Most job seekers apply to dozens of companies across LinkedIn, company websites, and email — then lose track of where they stand. ApplyMate solves that by bringing your entire job search into Slack, where your day already happens.

---

## Commands

| Command | Description | Example |
|---|---|---|
| `/apply Company, Role` | Log a new job application | `/apply Google, Software Engineer` |
| `/mystatus` | View all your logged applications | `/mystatus` |
| `/update Number, Status` | Update an application status | `/update 1, Interview` |

### Available Statuses
- 🟡 Applied
- 🔵 Interview
- 🟢 Offer
- 🔴 Rejected
- ⚪ Withdrawn

---

## Tech Stack

- Python 3
- Slack Bolt
- Slack SDK
- Flask
- python-dotenv

---

## Local Setup

### 1. Clone the repo
```bash
git clone https://github.com/Benita232/applymate.git
cd applymate
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here

### 5. Run the app
```bash
python main.py
```

### 6. Expose with ngrok
```bash
ngrok http --url=your-ngrok-url 3000
```

---

## Project Structure
applymate/
├── app/
│   ├── init.py
│   ├── commands/
│   │   ├── init.py
│   │   ├── apply.py
│   │   ├── status.py
│   │   └── update.py
│   └── storage/
│       └── db.py
├── main.py
├── .env
└── requirements.txt

---

## How it works

1. User types a slash command in any Slack channel
2. Slack sends the request to the Flask server via ngrok
3. Slack Bolt processes the command and routes it to the correct handler
4. The handler reads or writes to a local JSON database
5. A structured Block Kit response is sent back to the user in Slack

---

## Built by

Benita Nnabuife — [GitHub](https://github.com/Benita232) • [LinkedIn](https://linkedin.com/in/benita-nnabuife-3a67a5231) • [Website](https://benitatechhub.co.za)