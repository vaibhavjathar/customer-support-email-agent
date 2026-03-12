"""Node for generating customer support responses."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState
from src.services.llm_service import LLMService
from src.services.knowledge_service import KnowledgeService

logger = logging.getLogger(__name__)


def generate_response_node(state: AgentState) -> Dict[str, Any]:
    """Generate a response to the customer email.

    Reads: email_subject, email_body, email_classification, retrieved_knowledge
    Updates: generated_response, confidence_score, processing_steps, errors
    Returns: dict with updates only
    """
    llm_service = LLMService()
    knowledge_service = KnowledgeService()

    try:
        # Get full knowledge context
        knowledge_context = ""
        if state.get("retrieved_knowledge"):
            # Search again to get full articles for context
            articles = knowledge_service.search_knowledge_base(
                query=" ".join(state["retrieved_knowledge"][:3]),
                category=state.get("email_classification"),
            )
            knowledge_context = knowledge_service.format_knowledge_context(articles)

        # Generate response
        response = llm_service.generate_response(
            subject=state["email_subject"],
            body=state["email_body"],
            category=state.get("email_classification") or "general",
            knowledge_context=knowledge_context,
        )

        logger.info("Response generated successfully")

        # Calculate initial confidence score (will be refined in assess_priority)
        confidence_score = 0.8 if knowledge_context else 0.6

        return {
            "generated_response": response,
            "confidence_score": confidence_score,
            "processing_steps": ["generate_response"],
        }

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return {
            "generated_response": "Unable to generate response at this time. Please contact support.",
            "confidence_score": 0.3,
            "processing_steps": ["generate_response"],
            "errors": [f"Response generation error: {str(e)}"],
        }
