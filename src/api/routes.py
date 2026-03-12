"""API routes for email processing."""
import uuid
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from src.schemas.email import EmailRequest, EmailResponse
from src.services.email_service import EmailService
from src.services.db_service import DBService
from src.graph import build_email_support_graph

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["emails"])

email_service = EmailService()
db_service = DBService()
support_graph = build_email_support_graph()


@router.post("/process-email", response_model=EmailResponse)
def process_email(request: EmailRequest) -> EmailResponse:
    """Process an incoming customer support email.

    Accepts EmailRequest with keys:
    - email_from: sender email
    - email_to: recipient email
    - email_subject: subject line
    - email_body: email body content
    - customer_name: (optional) customer name
    - customer_id: (optional) customer ID

    Returns EmailResponse with:
    - email_id: unique email ID
    - email_subject: subject line
    - generated_response: AI-generated response
    - email_classification: category (billing, technical, etc.)
    - confidence_score: confidence in response (0-1)
    - requires_human_review: whether escalation needed
    - suggested_actions: recommended next steps
    - processing_steps: workflow steps completed
    - errors: any errors encountered
    """
    try:
        # Generate unique email ID
        email_id = str(uuid.uuid4())

        # Log incoming email
        logger.info(
            f"Processing email {email_id} from {request.email_from} "
            f"with subject: {request.email_subject[:50]}"
        )

        # Initialize AgentState as a dictionary (TypedDict)
        initial_state = {
            "email_from": request.email_from,
            "email_to": request.email_to,
            "email_subject": request.email_subject,
            "email_body": request.email_body,
            "customer_id": request.customer_id,
            "customer_name": request.customer_name,
        }

        # Invoke the compiled graph with synchronous invoke
        result = support_graph.invoke(initial_state)

        # Log processing completion
        logger.info(
            f"Email {email_id} processed. "
            f"Classification: {result.get('email_classification')}, "
            f"Requires review: {result.get('requires_human_review')}"
        )

        # Update email in service
        email_service.update_email_status(
            email_id=email_id,
            status="processed",
            response=result.get("generated_response"),
        )

        # Save email record to database
        db_service.save_email_record({
            "id": email_id,
            "email_from": request.email_from,
            "email_subject": request.email_subject,
            "email_body": request.email_body,
            "classification": result.get("email_classification"),
            "generated_response": result.get("generated_response") or "",
            "requires_human_review": result.get("requires_human_review", False),
        })

        # Build and return response using bracket notation
        return EmailResponse(
            email_id=email_id,
            email_subject=f"Re: {request.email_subject}",
            generated_response=result.get("generated_response") or "",
            confidence_score=result.get("confidence_score"),
            email_classification=result.get("email_classification"),
            requires_human_review=result.get("requires_human_review", False),
            retrieved_knowledge=result.get("retrieved_knowledge"),
            suggested_actions=result.get("suggested_actions"),
            processing_steps=result.get("processing_steps"),
            errors=result.get("errors"),
        )

    except Exception as e:
        logger.error(f"Error processing email: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing email: {str(e)}"
        )


@router.get("/emails/{email_id}")
def get_email(email_id: str):
    """Retrieve email by ID from database."""
    try:
        email = db_service.get_email(email_id)
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        return {
            "id": email.id,
            "email_from": email.email_from,
            "email_subject": email.email_subject,
            "email_body": email.email_body,
            "classification": email.classification,
            "generated_response": email.generated_response,
            "requires_human_review": email.requires_human_review,
            "created_at": email.created_at.isoformat(),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving email {email_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving email")


@router.get("/emails")
def list_emails(limit: int = 100, offset: int = 0):
    """List emails from database with pagination.

    Query parameters:
    - limit: maximum number of emails to return (default: 100)
    - offset: number of emails to skip (default: 0)
    """
    try:
        records = db_service.get_all_emails(limit=limit, offset=offset)
        emails = [
            {
                "id": record.id,
                "email_from": record.email_from,
                "email_subject": record.email_subject,
                "email_body": record.email_body,
                "classification": record.classification,
                "generated_response": record.generated_response,
                "requires_human_review": record.requires_human_review,
                "created_at": record.created_at.isoformat(),
            }
            for record in records
        ]
        return {"emails": emails, "count": len(emails)}
    except Exception as e:
        logger.error(f"Error retrieving emails: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving emails")
