"""SQLAlchemy models for the application."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Text

from src.db.database import Base


class EmailRecord(Base):
    """Email record model for audit trail persistence."""

    __tablename__ = "email_records"

    id = Column(String, primary_key=True, index=True)
    email_from = Column(String, index=True)
    email_subject = Column(String, index=True)
    email_body = Column(Text)
    classification = Column(String, index=True)
    generated_response = Column(Text)
    requires_human_review = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<EmailRecord(id={self.id}, from={self.email_from}, classification={self.classification})>"
