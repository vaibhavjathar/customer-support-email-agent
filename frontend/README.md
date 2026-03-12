# Customer Support Email Agent - Streamlit Frontend

A beautiful, interactive web interface for testing the Customer Support Email Agent.

## Features

- **✉️ Send Mock Email Page**: Submit test emails and watch the AI agent process them in real-time
- **📥 Agent Inbox Dashboard**: View all processed emails with detailed analytics
- **Smart Filtering**: Filter emails by classification and review status
- **Color-Coded Badges**: Visual indicators for email types and review requirements
- **Responsive Design**: Works on desktop and tablet devices

## Prerequisites

- Python 3.8+
- Backend server running at `http://localhost:8000`
- All dependencies installed (see requirements.txt)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure the backend API is running:
```bash
# In another terminal
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Running the Frontend

Start the Streamlit app:
```bash
streamlit run frontend/app.py
```

The app will open at `http://localhost:8501`

## Architecture

The frontend is completely decoupled from the backend and communicates exclusively via HTTP REST APIs:

- **POST `/api/v1/process-email`** - Submit an email for processing
- **GET `/api/v1/emails`** - Retrieve all processed emails
- **GET `/api/v1/emails/{email_id}`** - Retrieve a specific email

## Pages

### Page 1: Send Mock Email
- Fill in email details (from, to, subject, body)
- Submit to the API
- View classification, generated response, and retrieved knowledge
- See full JSON response for debugging

### Page 2: Agent Inbox
- View all processed emails in your database
- Filter by classification (billing, technical, account, etc.)
- See emails flagged for human review
- Expand each email to view original content and AI response
- Track metrics: total emails, emails needing review, by category

## Configuration

The backend API URL is hardcoded to `http://localhost:8000/api/v1`. To change it, edit the `API_BASE_URL` variable in `frontend/app.py`.
