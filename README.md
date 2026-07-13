Here's the updated README — replace everything with this:

```markdown
# ApplyMate 🎯

> Your AI-powered job search co-pilot inside Slack.

ApplyMate is a Slack agent that helps job seekers track every application and get AI-powered suggestions — all without leaving Slack. Log applications, check your progress, update statuses, and get intelligent next-step advice using simple slash commands.

Built for the **Devpost Slack Agent Builder Challenge 2026**.

---

## What it does

Most job seekers apply to dozens of companies across LinkedIn, company websites, and email — then lose track of where they stand. ApplyMate solves that by bringing your entire job search into Slack, where your day already happens. With built-in Gemini AI suggestions, ApplyMate doesn't just track your applications — it coaches you on what to do next.

---

## User Stories

**As a job seeker**, I want to log a new application instantly so I don't forget where I applied.

**As a job seeker**, I want to view all my applications in one place so I can see exactly where I stand at a glance.

**As a job seeker**, I want to update an application status so I can track my progress from Applied to Interview to Offer.

**As a job seeker**, I want AI-powered suggestions so I know what to do next in my job search.

---

## Commands

| Command | Description | Example |
|---|---|---|
| `/apply Company, Role` | Log a new job application | `/apply Google, Software Engineer` |
| `/mystatus` | View all your logged applications | `/mystatus` |
| `/update Number, Status` | Update an application status | `/update 1, Interview` |
| `/delete Number` | Delete an application | `/delete 2` |
| `/suggest` | Get AI-powered job search suggestions | `/suggest` |

### Available Statuses
- 🟡 Applied
- 🔵 Interview
- 🟢 Offer
- 🔴 Rejected
- ⚪ Withdrawn

---

## AI Capability

ApplyMate uses **Google Gemini AI** to analyse your current applications and provide personalised, actionable job search coaching. The `/suggest` command sends your application data to Gemini and returns specific next steps tailored to where you are in your job search.

---

## Tech Stack

- Python 3
- Slack Bolt
- Slack SDK
- Flask
- Google Generative AI (Gemini)
- python-dotenv
- ngrok (for local development)

---

## How to Run Locally

### Prerequisites
- Python 3.x installed
- A Slack workspace
- A Slack app with slash commands configured
- ngrok installed
- Google Gemini API key

### 1. Clone the repo
```bash
git clone https://github.com/Benita232/applymate.git
cd applymate
```

### 2. Create and activate virtual environment
```bash
# Create venv
python -m venv venv

# Activate on Windows PowerShell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Users\benit\Downloads\applymate\venv\Scripts\Activate.ps1)

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
GEMINI_API_KEY=your-gemini-api-key-here
```

### 5. Start the Flask server
Open Terminal 1 and run:
```bash
python main.py
```

### 6. Start ngrok tunnel
Open Terminal 2 and run:
```bash
ngrok http --url=your-ngrok-url 3000
```

### 7. Configure Slack slash commands
Set the Request URL for all commands to:
```
https://your-ngrok-url.ngrok-free.dev/slack/events
```

### 8. Test in Slack
```
/apply Google, Software Engineer
/apply Meta, Data Engineer
/mystatus
/update 1, Interview
/suggest
/delete 2
/mystatus
```

---

## For Judges

To test ApplyMate live in the Slack sandbox:

1. Accept the workspace invite sent to slackhack@salesforce.com
   and testing@devpost.com
2. Open the **corestack studio** Slack workspace
3. Go to the **testing-applymate** channel and type:
   ```
   /apply Google, Software Engineer
   /mystatus
   /update 1, Interview
   /suggest
   ```

> **Note:** The bot runs on a local server via ngrok.
> If the bot does not respond, the server may be offline.
> Please watch the demo video for a full walkthrough of
> the working project.

---

## Project Structure

```
applymate/
├── app/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── apply.py
│   │   ├── status.py
│   │   ├── update.py
│   │   ├── delete.py
│   │   └── suggest.py
│   └── storage/
│       └── db.py
├── main.py
├── .env
└── requirements.txt
```

---

## How it works

1. User types a slash command in any Slack channel
2. Slack sends the request to the Flask server via ngrok
3. Slack Bolt processes the command and routes it to the correct handler
4. The handler reads or writes to a local JSON database
5. For `/suggest`, application data is sent to Gemini AI for analysis
6. A structured Block Kit response is sent back to the user in Slack

---

## Built by

Benita Nnabuife — [GitHub](https://github.com/Benita232) • [LinkedIn](https://linkedin.com/in/benita-nnabuife-3a67a5231) • [Website](https://benitatechhub.co.za)
```
