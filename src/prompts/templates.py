"""Prompt templates for various tasks in the customer support workflow."""

CLASSIFICATION_PROMPT = """You are a customer support email classifier.
Analyze the following customer support email and classify it into one of the following categories:

Categories:
- billing: Issues related to payment, invoicing, subscriptions
- technical: Technical issues, bugs, feature requests
- account: Account management, login, password reset
- general: General inquiries and information requests
- complaint: Customer complaints and dissatisfaction
- refund: Refund requests
- other: Anything that doesn't fit above

Email Subject: {subject}
Email Body: {body}

Respond with ONLY the category name, nothing else."""

RESPONSE_GENERATION_PROMPT = """You are a professional customer support agent.
Generate a helpful, empathetic, and professional response to the following customer email.

Customer Email:
Subject: {subject}
Body: {body}

Category: {category}

{knowledge_context}

Requirements:
- Be concise but comprehensive
- Show empathy and understanding
- Provide clear solutions or next steps
- Maintain a professional tone
- If you need more information, ask specific questions

Generate the response:"""

KNOWLEDGE_RETRIEVAL_PROMPT = """Based on the following customer support email, identify what knowledge base articles or FAQs would be most helpful.

Email Subject: {subject}
Email Body: {body}
Category: {category}

Identify 3-5 relevant knowledge base topics or search terms that would help resolve this issue.
Format as a comma-separated list."""

SENTIMENT_ANALYSIS_PROMPT = """Analyze the sentiment and urgency level of the following customer email.

Email Subject: {subject}
Email Body: {body}

Provide analysis with:
- sentiment: (positive, neutral, or negative)
- urgency: (low, medium, or high)
- frustration_level: (1-5, where 5 is most frustrated)
- key_concerns: (list of main issues mentioned)"""

PRIORITY_ASSESSMENT_PROMPT = """Assess the priority level of this customer support email.

Email Subject: {subject}
Email Body: {body}
Category: {category}
Sentiment: {sentiment}
Urgency: {urgency}

Determine if this requires:
1. Immediate response (priority: high)
2. Response within 24 hours (priority: medium)
3. Response within 48 hours (priority: low)

Also indicate if it requires human review or escalation.

Provide assessment with:
- priority_level: high, medium, or low
- requires_human_review: true or false (boolean, not string)
- reason: brief explanation of your assessment"""

SUMMARY_PROMPT = """Create a brief summary of this customer support conversation.

Subject: {subject}
Customer Email: {customer_email}
Generated Response: {generated_response}

Provide a 2-3 sentence summary covering:
- What the customer issue was
- What solution/response was provided

Summary:"""

ESCALATION_PROMPT = """Determine if this customer support email should be escalated to human support.

Email Subject: {subject}
Email Body: {body}
Category: {category}
Sentiment Analysis: {sentiment_analysis}

Consider escalation for:
- Complex technical issues requiring deep expertise
- Billing disputes
- Complaints requiring manager review
- Issues outside standard support scope
- Unclear problems needing clarification

Provide assessment with:
- should_escalate: (true or false)
- escalation_reason: (brief reason if true)
- suggested_department: (if escalating, which team)"""
