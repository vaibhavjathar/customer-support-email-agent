"""Email-related schemas."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Email(BaseModel):
    """Email message model."""

    id: Optional[str] = None
    email_from: str
    email_to: str
    email_subject: str
    email_body: str
    received_at: Optional[datetime] = None
    tags: Optional[list[str]] = None


class EmailRequest(BaseModel):
    """Request model for processing an email.

    Keys MUST match AgentState exactly:
    - email_from: sender email address
    - email_to: recipient email address
    - email_subject: email subject line
    - email_body: email body content
    """

    email_from: str
    email_to: str
    email_subject: str
    email_body: str
    customer_name: Optional[str] = None
    customer_id: Optional[str] = None


class EmailResponse(BaseModel):
    """Response model for email processing."""

    email_id: str
    email_subject: str
    generated_response: str
    confidence_score: Optional[float] = None
    email_classification: Optional[str] = None
    requires_human_review: bool = False
    retrieved_knowledge: Optional[list[str]] = None
    suggested_actions: Optional[list[str]] = None
    processing_steps: Optional[list[str]] = None
    errors: Optional[list[str]] = None
