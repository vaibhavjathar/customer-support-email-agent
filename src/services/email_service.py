"""Email service for email processing and management."""
import logging
from datetime import datetime
from typing import Optional
import uuid

logger = logging.getLogger(__name__)


class EmailService:
    """Service for email processing and storage."""

    def __init__(self):
        """Initialize email service."""
        self.emails = {}  # Simple in-memory storage for now

    def parse_email(self, from_email: str, to_email: str, subject: str, body: str) -> dict:
        """Parse and store incoming email."""
        email_id = str(uuid.uuid4())

        email_data = {
            "id": email_id,
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "body": body,
            "received_at": datetime.now().isoformat(),
            "status": "received",
        }

        self.emails[email_id] = email_data
        logger.info(f"Email parsed and stored: {email_id}")
        return email_data

    def get_email(self, email_id: str) -> dict:
        """Retrieve email by ID."""
        return self.emails.get(email_id)

    def update_email_status(self, email_id: str, status: str, response: Optional[str] = None):
        """Update email status and response."""
        if email_id in self.emails:
            self.emails[email_id]["status"] = status
            if response:
                self.emails[email_id]["response"] = response
                self.emails[email_id]["responded_at"] = datetime.now().isoformat()
            logger.info(f"Email {email_id} status updated to: {status}")

    def list_emails(self, status: Optional[str] = None) -> list[dict]:
        """List emails, optionally filtered by status."""
        if status:
            return [e for e in self.emails.values() if e["status"] == status]
        return list(self.emails.values())
