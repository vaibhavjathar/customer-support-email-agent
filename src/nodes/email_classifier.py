"""Node for email classification."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState
from src.services.llm_service import LLMService

logger = logging.getLogger(__name__)


def classify_email_node(state: AgentState) -> Dict[str, Any]:
    """Classify incoming email into a category.

    Reads: email_subject, email_body
    Updates: email_classification, processing_steps, errors
    Returns: dict with updates only
    """
    llm_service = LLMService()

    try:
        classification = llm_service.classify_email(
            subject=state["email_subject"],
            body=state["email_body"],
        )
        logger.info(f"Email classified as: {classification}")

        return {
            "email_classification": classification,
            "processing_steps": ["classify_email"],
        }
    except Exception as e:
        logger.error(f"Error classifying email: {str(e)}")
        return {
            "email_classification": "other",
            "processing_steps": ["classify_email"],
            "errors": [f"Classification error: {str(e)}"],
        }
