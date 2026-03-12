"""Node for human review routing."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState

logger = logging.getLogger(__name__)


def human_review_node(state: AgentState) -> Dict[str, Any]:
    """Route case to human agent for review.

    Reads: email_classification, email_subject, generated_response
    Updates: processing_steps, conversation_history
    Returns: dict with updates only
    """
    try:
        classification = state.get("email_classification", "unknown")
        subject = state.get("email_subject", "No subject")

        logger.info(
            f"Case routed to human review: {classification} - {subject[:50]}"
        )

        return {
            "processing_steps": ["human_review"],
            "conversation_history": [{
                "step": "human_review_routed",
                "classification": classification,
                "subject": subject,
                "timestamp": None,  # Could be added
            }],
        }

    except Exception as e:
        logger.error(f"Error in human review routing: {str(e)}")
        return {
            "processing_steps": ["human_review"],
            "errors": [f"Human review routing error: {str(e)}"],
        }