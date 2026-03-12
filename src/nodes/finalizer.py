"""Node for finalizing the workflow and preparing output."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState

logger = logging.getLogger(__name__)


def finalize_node(state: AgentState) -> Dict[str, Any]:
    """Finalize the workflow and prepare output.

    Reads: email_classification, requires_human_review, processing_steps, errors
    Updates: suggested_actions, processing_steps
    Returns: dict with updates only
    """
    try:
        # Generate suggested actions based on classification
        suggested_actions = _get_suggested_actions(
            classification=state.get("email_classification") or "other",
            requires_review=state.get("requires_human_review", False),
        )

        logger.info(f"Workflow finalized. {len(suggested_actions)} actions suggested.")

        return {
            "suggested_actions": suggested_actions,
            "processing_steps": ["finalize"],
        }

    except Exception as e:
        logger.error(f"Error in finalization: {str(e)}")
        return {
            "suggested_actions": ["Manual review required"],
            "processing_steps": ["finalize"],
            "errors": [f"Finalization error: {str(e)}"],
        }


def _get_suggested_actions(classification: str, requires_review: bool) -> list[str]:
    """Generate suggested actions based on email classification."""
    actions = []

    if classification == "billing":
        actions.append("Review billing records")
        actions.append("Verify payment method on file")

    elif classification == "technical":
        actions.append("Check system logs")
        actions.append("Verify API integration")

    elif classification == "account":
        actions.append("Verify account ownership")
        actions.append("Check security settings")

    elif classification == "complaint":
        actions.append("Escalate to management")
        actions.append("Prepare apology and resolution")

    elif classification == "refund":
        actions.append("Review refund policy")
        actions.append("Process refund if eligible")

    if requires_review:
        actions.insert(0, "Route to human agent for review")

    return actions if actions else ["Send generated response", "Log interaction"]
