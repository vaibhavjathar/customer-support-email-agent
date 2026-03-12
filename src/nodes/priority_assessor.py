"""Node for assessing priority and escalation needs."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState
from src.services.llm_service import LLMService

logger = logging.getLogger(__name__)


def assess_priority_node(state: AgentState) -> Dict[str, Any]:
    """Assess priority and determine if human review is needed.

    Reads: email_subject, email_body, email_classification, sentiment_data, confidence_score
    Updates: requires_human_review, processing_steps, conversation_history, errors
    Returns: dict with updates only
    """
    llm_service = LLMService()

    try:
        # Get sentiment data
        sentiment_data = state.get("sentiment_data", {})

        # Assess priority
        priority_assessment = llm_service.assess_priority(
            subject=state["email_subject"],
            body=state["email_body"],
            category=state.get("email_classification") or "general",
            sentiment=sentiment_data.get("sentiment", "neutral"),
            urgency=sentiment_data.get("urgency", "medium"),
        )

        # Determine if human review is needed based on:
        # 1. LLM assessment
        # 2. Confidence score (if low, escalate)
        # 3. High urgency or complexity
        requires_review = priority_assessment.get("requires_human_review", False)
        confidence = state.get("confidence_score", 0.5)

        if confidence < 0.5 or priority_assessment.get("priority_level") == "high":
            requires_review = True

        logger.info(
            f"Priority assessed: {priority_assessment.get('priority_level', 'unknown')} "
            f"(requires_review: {requires_review})"
        )

        return {
            "requires_human_review": requires_review,
            "processing_steps": ["assess_priority"],
            "conversation_history": [{
                "step": "priority_assessment",
                "data": priority_assessment,
            }],
        }

    except Exception as e:
        logger.error(f"Error assessing priority: {str(e)}")
        # On error, escalate to human review
        return {
            "requires_human_review": True,
            "processing_steps": ["assess_priority"],
            "errors": [f"Priority assessment error: {str(e)}"],
        }
