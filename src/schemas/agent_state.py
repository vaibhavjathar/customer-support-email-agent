"""LangGraph agent state schema."""
import operator
from typing import TypedDict, Optional, Annotated
from typing_extensions import NotRequired


def _add_list(a: list, b: list) -> list:
    """Reducer for list fields - appends new items."""
    return a + b if a else b


class AgentState(TypedDict):
    """State for LangGraph workflow.

    All fields use bracket notation for access.
    List fields accumulate with operator.add reducer.
    """

    # Email input (required)
    email_from: str
    email_to: str
    email_subject: str
    email_body: str

    # Customer metadata (optional)
    customer_id: NotRequired[Optional[str]]
    customer_name: NotRequired[Optional[str]]

    # Processing state
    email_classification: NotRequired[Optional[str]]
    retrieved_knowledge: NotRequired[Annotated[list[str], _add_list]]
    sentiment_data: NotRequired[dict]

    # Output
    generated_response: NotRequired[Optional[str]]
    confidence_score: NotRequired[Optional[float]]
    requires_human_review: NotRequired[bool]
    suggested_actions: NotRequired[Annotated[list[str], _add_list]]

    # Metadata (list fields with operator.add reducer)
    processing_steps: NotRequired[Annotated[list[str], _add_list]]
    errors: NotRequired[Annotated[list[str], _add_list]]
    conversation_history: NotRequired[Annotated[list[dict], _add_list]]
