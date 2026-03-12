"""Email support workflow using LangGraph.

Business Flow:
1. Ingest & Read: START
2. Classify Intent: classify_email_node
3. Analyze Sentiment: analyze_sentiment_node
4. Knowledge Retrieval: retrieve_knowledge_node
5. Draft Response: generate_response_node
6. Assess Priority: assess_priority_node
7. Conditional Routing: human_review_node OR finalize_node
8. Finalize: finalize_node
9. Complete: END
"""
import operator
from langgraph.graph import StateGraph, START, END

from src.schemas.agent_state import AgentState
from src.nodes import (
    classify_email_node,
    analyze_sentiment_node,
    retrieve_knowledge_node,
    generate_response_node,
    assess_priority_node,
    human_review_node,
    finalize_node,
)


def build_email_support_graph():
    """Build the email support processing workflow graph.

    Implements the business flow with proper state management:
    - All nodes use bracket notation for state access
    - All nodes return dictionaries for state updates
    - List fields use operator.add for accumulation
    - Conditional routing based on requires_human_review
    """
    # Create workflow with state reducers
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("classify_email", classify_email_node)
    workflow.add_node("analyze_sentiment", analyze_sentiment_node)
    workflow.add_node("retrieve_knowledge", retrieve_knowledge_node)
    workflow.add_node("generate_response", generate_response_node)
    workflow.add_node("assess_priority", assess_priority_node)
    workflow.add_node("human_review", human_review_node)
    workflow.add_node("finalize", finalize_node)

    # Define the workflow edges with START and END
    workflow.add_edge(START, "classify_email")
    workflow.add_edge("classify_email", "analyze_sentiment")
    workflow.add_edge("analyze_sentiment", "retrieve_knowledge")
    workflow.add_edge("retrieve_knowledge", "generate_response")
    workflow.add_edge("generate_response", "assess_priority")

    # Conditional edge: route to human review or finalize based on requires_human_review
    workflow.add_conditional_edges(
        "assess_priority",
        _route_to_review,
        {
            "human_review": "human_review",
            "finalize": "finalize",
        },
    )

    # Both paths converge at finalize
    workflow.add_edge("human_review", "finalize")
    workflow.add_edge("finalize", END)

    # Compile the graph
    graph = workflow.compile()

    return graph


def _route_to_review(state: AgentState) -> str:
    """Determine if case should go to human review or be finalized.

    Args:
        state: Current graph state

    Returns:
        "human_review" if human review is needed, "finalize" otherwise
    """
    requires_review = state.get("requires_human_review", False)

    if requires_review:
        return "human_review"
    else:
        return "finalize"
