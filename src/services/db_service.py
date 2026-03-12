"""Database service for email records persistence."""
import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.db.database import SessionLocal
from src.db.models import EmailRecord

logger = logging.getLogger(__name__)


class DBService:
    """Service for managing email records in the database."""

    def __init__(self):
        """Initialize database service."""
        self.db = SessionLocal()

    def save_email_record(self, data: dict) -> EmailRecord:
        """Save an email record to the database.

        Args:
            data: Dictionary containing email data with keys:
                - id: Email ID
                - email_from: Sender email
                - email_subject: Email subject
                - email_body: Email body
                - classification: Email classification
                - generated_response: Generated response
                - requires_human_review: Whether it needs human review

        Returns:
            Created EmailRecord instance
        """
        try:
            email_record = EmailRecord(
                id=data.get("id"),
                email_from=data.get("email_from"),
                email_subject=data.get("email_subject"),
                email_body=data.get("email_body"),
                classification=data.get("classification"),
                generated_response=data.get("generated_response"),
                requires_human_review=data.get("requires_human_review", False),
            )
            self.db.add(email_record)
            self.db.commit()
            self.db.refresh(email_record)

            logger.info(f"Email record saved: {email_record.id}")
            return email_record
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving email record: {str(e)}")
            raise

    def get_email(self, email_id: str) -> Optional[EmailRecord]:
        """Retrieve an email record by ID.

        Args:
            email_id: Email ID

        Returns:
            EmailRecord if found, None otherwise
        """
        try:
            record = self.db.query(EmailRecord).filter(EmailRecord.id == email_id).first()
            if record:
                logger.info(f"Retrieved email record: {email_id}")
            else:
                logger.warning(f"Email record not found: {email_id}")
            return record
        except Exception as e:
            logger.error(f"Error retrieving email record: {str(e)}")
            raise

    def get_all_emails(self, limit: int = 100, offset: int = 0) -> list[EmailRecord]:
        """Retrieve all email records with pagination.

        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of EmailRecord instances
        """
        try:
            records = (
                self.db.query(EmailRecord)
                .order_by(EmailRecord.created_at.desc())
                .limit(limit)
                .offset(offset)
                .all()
            )
            logger.info(f"Retrieved {len(records)} email records")
            return records
        except Exception as e:
            logger.error(f"Error retrieving email records: {str(e)}")
            raise

    def close(self):
        """Close the database session."""
        self.db.close()
