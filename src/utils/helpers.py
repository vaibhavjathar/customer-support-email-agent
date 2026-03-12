"""Helper utility functions."""
import re
from typing import Optional


def sanitize_email(email: str) -> str:
    """Sanitize and validate email address."""
    # Basic email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_pattern, email.strip()):
        return email.strip().lower()
    raise ValueError(f"Invalid email format: {email}")


def extract_email_domain(email: str) -> str:
    """Extract domain from email address."""
    try:
        domain = email.split("@")[1]
        return domain
    except IndexError:
        raise ValueError(f"Invalid email format: {email}")


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length with ellipsis."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def format_response_for_email(response: str) -> str:
    """Format LLM response for email delivery."""
    # Add signature placeholder
    signature = "\n\nBest regards,\nCustomer Support Team"
    return response + signature


def parse_email_body(body: str) -> dict:
    """Parse email body and extract key information."""
    lines = body.split("\n")
    return {
        "lines": lines,
        "word_count": len(body.split()),
        "line_count": len(lines),
        "has_links": "http" in body.lower(),
    }
