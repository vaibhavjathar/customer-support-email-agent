"""Node for knowledge base retrieval."""
import logging
from typing import Dict, Any

from src.schemas.agent_state import AgentState
from src.services.llm_service import LLMService
from src.services.knowledge_service import KnowledgeService

logger = logging.getLogger(__name__)


def retrieve_knowledge_node(state: AgentState) -> Dict[str, Any]:
    """Retrieve relevant knowledge base articles using FAISS RAG.

    Reads state via bracket notation:
    - email_subject: email subject line
    - email_body: email body content
    - email_classification: email category

    Updates state with:
    - retrieved_knowledge: list of relevant document titles
    - processing_steps: workflow step tracking
    - conversation_history: step metadata
    - errors: any errors encountered

    Returns: dict with updates only (no state mutation)
    """
    llm_service = LLMService()
    knowledge_service = KnowledgeService()

    try:
        # Generate knowledge queries based on email using LLM
        queries = llm_service.retrieve_knowledge_queries(
            subject=state["email_subject"],
            body=state["email_body"],
            category=state.get("email_classification") or "general",
        )

        logger.info(f"Generated {len(queries)} knowledge queries for RAG search")

        # Search knowledge base for each query using FAISS vector similarity
        all_articles = []
        for query in queries:
            articles = knowledge_service.search_knowledge_base(
                query=query,
                category=state.get("email_classification"),
                top_k=3,
            )
            all_articles.extend(articles)

        # Extract titles for state (remove duplicates while preserving order)
        seen = set()
        retrieved_titles = []
        for article in all_articles:
            if article["title"] not in seen:
                retrieved_titles.append(article["title"])
                seen.add(article["title"])

        logger.info(f"Retrieved {len(retrieved_titles)} unique knowledge base articles")

        return {
            "retrieved_knowledge": retrieved_titles,
            "processing_steps": ["retrieve_knowledge"],
            "conversation_history": [{
                "step": "knowledge_retrieval",
                "queries": queries,
                "articles_found": len(retrieved_titles),
                "faiss_rag": True,
            }],
        }

    except Exception as e:
        logger.error(f"Error retrieving knowledge: {str(e)}")
        return {
            "retrieved_knowledge": [],
            "processing_steps": ["retrieve_knowledge"],
            "errors": [f"Knowledge retrieval error: {str(e)}"],
        }
