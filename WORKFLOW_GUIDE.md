# Customer Support Email Agent - Workflow Guide

## Business Flow (Implemented)

The workflow follows this exact sequence:

```
START
  ↓
Classify Intent (classify_email_node)
  ↓
Analyze Sentiment (analyze_sentiment_node)
  ↓
Knowledge Retrieval (retrieve_knowledge_node)
  ↓
Draft Response (generate_response_node)
  ↓
Assess Priority (assess_priority_node)
  ↓
[Conditional Routing]
├─ If requires_human_review=True → Human Review (human_review_node)
│   ↓
│   Finalize (finalize_node)
│   ↓
│   END
│
└─ If requires_human_review=False → Finalize (finalize_node)
    ↓
    END
```

## Architectural Rules Enforced

### 1. **State is a TypedDict**
```python
class AgentState(TypedDict):
    email_from: str
    email_to: str
    email_subject: str
    email_body: str
    # ... other fields with NotRequired for optional ones
```

### 2. **Bracket Notation for State Access**
All nodes read state using bracket notation (not dot notation):
```python
# ✅ CORRECT
subject = state["email_subject"]
classification = state.get("email_classification", "other")

# ❌ WRONG
subject = state.email_subject
```

### 3. **Return Dictionaries Only**
Nodes return ONLY dictionaries containing keys to update:
```python
# ✅ CORRECT
def classify_email_node(state: AgentState) -> Dict[str, Any]:
    classification = llm_service.classify_email(...)
    return {
        "email_classification": classification,
        "processing_steps": ["classify_email"],
    }

# ❌ WRONG
def classify_email_node(state: AgentState) -> AgentState:
    state["email_classification"] = classification
    return state
```

### 4. **List Reducers with operator.add**
List fields accumulate using `operator.add`. Return **new items to append**, not the full list:
```python
# ✅ CORRECT - Return new items
return {
    "processing_steps": ["classify_email"],  # Gets appended
    "errors": ["Error message"],              # Gets appended
    "conversation_history": [{"step": "..."}],  # Gets appended
}

# ❌ WRONG - Don't replace the entire list
return {
    "processing_steps": ["classify_email", "sentiment_analysis"],  # Would lose prior steps
}
```

### 5. **Modern LangGraph with START/END**
The workflow uses modern LangGraph API:
```python
from langgraph.graph import StateGraph, START, END

workflow = StateGraph(AgentState, reducer=reducers)
workflow.add_edge(START, "classify_email")
workflow.add_conditional_edges("assess_priority", _route_to_review, {...})
workflow.add_edge("finalize", END)
```

## Node Responsibilities

### 1. Classify Email Node
- **Input**: email_subject, email_body
- **Output**: email_classification, processing_steps
- **Action**: Categorizes email (billing, technical, account, complaint, refund, general)

### 2. Analyze Sentiment Node
- **Input**: email_subject, email_body
- **Output**: sentiment_data, processing_steps, conversation_history
- **Action**: Detects sentiment, urgency, frustration level

### 3. Retrieve Knowledge Node
- **Input**: email_subject, email_body, email_classification
- **Output**: retrieved_knowledge, processing_steps, conversation_history
- **Action**: Searches knowledge base for relevant articles

### 4. Generate Response Node
- **Input**: email_subject, email_body, email_classification, retrieved_knowledge
- **Output**: generated_response, confidence_score, processing_steps
- **Action**: Creates professional response using LLM

### 5. Assess Priority Node
- **Input**: email_subject, email_body, email_classification, sentiment_data, confidence_score
- **Output**: requires_human_review, processing_steps, conversation_history
- **Action**: Determines if case needs human review based on:
  - LLM assessment
  - Confidence score (< 0.5 → escalate)
  - High urgency classification
  - Errors in processing

### 6. Human Review Node (Conditional)
- **Input**: email_classification, email_subject, generated_response
- **Output**: processing_steps, conversation_history
- **Action**: Routes case to human agent queue

### 7. Finalize Node
- **Input**: email_classification, requires_human_review, processing_steps, errors
- **Output**: suggested_actions, processing_steps
- **Action**: Generates recommended follow-up actions

## State Reducers Configuration

```python
reducers = {
    "processing_steps": operator.add,      # Append new steps
    "errors": operator.add,                # Append new errors
    "conversation_history": operator.add,  # Append new entries
    "retrieved_knowledge": operator.add,   # Append new articles
    "suggested_actions": operator.add,     # Append new actions
}
```

## Usage Example

```python
from src.graph import build_email_support_graph
from src.schemas.agent_state import AgentState

# Build the graph
graph = build_email_support_graph()

# Prepare initial state
initial_state = {
    "email_from": "customer@example.com",
    "email_to": "support@company.com",
    "email_subject": "Billing issue with my account",
    "email_body": "I was charged twice this month...",
    "customer_id": "cust_123",
    "customer_name": "John Doe",
}

# Run the workflow
result = graph.invoke(initial_state)

# Access results
print(f"Classification: {result['email_classification']}")
print(f"Requires Review: {result['requires_human_review']}")
print(f"Generated Response: {result['generated_response']}")
print(f"Suggested Actions: {result['suggested_actions']}")
print(f"Processing Steps: {result['processing_steps']}")
```

## Error Handling

Errors are accumulated in the state:
```python
result["errors"]  # List of all errors encountered
```

The workflow continues even if individual steps fail, with errors logged for later review.

## Conditional Routing Function

The `_route_to_review` function determines the path:

```python
def _route_to_review(state: AgentState) -> str:
    """Route to human review if needed."""
    requires_review = state.get("requires_human_review", False)
    return "human_review" if requires_review else "finalize"
```

This enables dynamic routing based on case complexity, urgency, and confidence.

## Key Points

1. ✅ All nodes are **synchronous** (no async)
2. ✅ All nodes use **bracket notation** for state
3. ✅ All nodes return **dictionaries** only
4. ✅ List fields **accumulate** with operator.add
5. ✅ **Conditional routing** based on business logic
6. ✅ **START and END** using modern LangGraph API
7. ✅ **Reducers** properly configured for list fields

## Testing the Workflow

```bash
# Run the application
python main.py

# Test via FastAPI
# POST http://localhost:8000/api/v1/process-email
# with email payload
```

See README.md for API usage examples.