"""Node for sentiment analysis."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState
from src.services.llm_service import LLMService

logger = logging.getLogger(__name__)


def analyze_sentiment_node(state: AgentState) -> Dict[str, Any]:
    """Analyze sentiment and urgency of the email.

    Reads: email_subject, email_body
    Updates: sentiment_data, processing_steps, conversation_history, errors
    Returns: dict with updates only
    """
    llm_service = LLMService()

    try:
        sentiment_data = llm_service.analyze_sentiment(
            subject=state["email_subject"],
            body=state["email_body"],
        )

        logger.info(f"Sentiment analysis: {sentiment_data.get('sentiment', 'unknown')}")

        return {
            "sentiment_data": sentiment_data,
            "processing_steps": ["analyze_sentiment"],
            "conversation_history": [{
                "step": "sentiment_analysis",
                "data": sentiment_data,
            }],
        }

    except Exception as e:
        logger.error(f"Error in sentiment analysis: {str(e)}")
        return {
            "processing_steps": ["analyze_sentiment"],
            "errors": [f"Sentiment analysis error: {str(e)}"],
        }
