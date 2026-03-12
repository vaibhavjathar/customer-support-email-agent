"""LLM service for interacting with Groq."""
import logging
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from src.core.config import settings

logger = logging.getLogger(__name__)


# ============================================================================
# Structured Output Models
# ============================================================================


class BooleanEnum(str, Enum):
    """Enum for boolean values to ensure Groq generates valid JSON."""

    TRUE = "true"
    FALSE = "false"

    def __bool__(self):
        """Convert to Python boolean."""
        return self.value == "true"


class ClassificationOutput(BaseModel):
    """Structured output for email classification."""

    category: str = Field(
        description="One of: billing, technical, account, complaint, refund, general"
    )


class SentimentOutput(BaseModel):
    """Structured output for sentiment analysis."""

    sentiment: str = Field(description="One of: positive, neutral, negative")
    urgency: str = Field(description="One of: low, medium, high")
    frustration_level: int = Field(
        description="Integer from 1-5 where 5 is most frustrated", ge=1, le=5
    )
    key_concerns: list[str] = Field(
        description="Array of issue strings mentioned by customer"
    )


class PriorityOutput(BaseModel):
    """Structured output for priority assessment."""

    priority_level: str = Field(
        description="One of: high, medium, low"
    )
    requires_human_review: BooleanEnum = Field(
        description="BooleanEnum: true or false (not string)"
    )
    reason: str = Field(
        description="String explanation of priority decision"
    )

    @field_validator("requires_human_review", mode="before")
    @classmethod
    def coerce_bool_enum(cls, v):
        """Convert boolean or string to BooleanEnum."""
        if isinstance(v, bool):
            return BooleanEnum.TRUE if v else BooleanEnum.FALSE
        if isinstance(v, str):
            return BooleanEnum.TRUE if v.lower() in ("true", "yes", "1") else BooleanEnum.FALSE
        return v


class KnowledgeQueryOutput(BaseModel):
    """Structured output for knowledge retrieval queries."""

    queries: list[str] = Field(
        description="Array of 3-5 search query strings for knowledge base"
    )


# ============================================================================
# LLM Service
# ============================================================================


class LLMService:
    """Service for LLM interactions using structured outputs."""

    def __init__(self):
        """Initialize the LLM service."""
        self.llm = ChatGroq(
            model=settings.groq_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            api_key=settings.groq_api_key,
        )

    def classify_email(self, subject: str, body: str) -> str:
        """Classify an email into a category.

        Args:
            subject: Email subject line
            body: Email body content

        Returns:
            Category string (billing, technical, account, complaint, refund, general)
        """
        from src.prompts import CLASSIFICATION_PROMPT

        # Create structured LLM
        structured_llm = self.llm.with_structured_output(ClassificationOutput)

        prompt = CLASSIFICATION_PROMPT.format(subject=subject, body=body)
        message = HumanMessage(content=prompt)

        response = structured_llm.invoke([message])
        classification = response.category.lower()

        logger.info(f"Email classified as: {classification}")
        return classification

    def generate_response(
        self,
        subject: str,
        body: str,
        category: str,
        knowledge_context: Optional[str] = None,
    ) -> str:
        """Generate a response to a customer email.

        Args:
            subject: Email subject line
            body: Email body content
            category: Email classification
            knowledge_context: Relevant knowledge base information

        Returns:
            Generated response text
        """
        from src.prompts import RESPONSE_GENERATION_PROMPT

        knowledge_text = ""
        if knowledge_context:
            knowledge_text = f"Relevant Knowledge Base:\n{knowledge_context}"

        prompt = RESPONSE_GENERATION_PROMPT.format(
            subject=subject,
            body=body,
            category=category,
            knowledge_context=knowledge_text,
        )
        message = HumanMessage(content=prompt)

        # Use plain LLM for response generation (returns text, not structured)
        response = self.llm.invoke([message])
        generated_response = response.content.strip()

        logger.info("Response generated successfully")
        return generated_response

    def analyze_sentiment(self, subject: str, body: str) -> dict:
        """Analyze sentiment and urgency of an email.

        Args:
            subject: Email subject line
            body: Email body content

        Returns:
            Dictionary with sentiment, urgency, frustration_level, key_concerns
        """
        from src.prompts import SENTIMENT_ANALYSIS_PROMPT

        # Create structured LLM
        structured_llm = self.llm.with_structured_output(SentimentOutput)

        prompt = SENTIMENT_ANALYSIS_PROMPT.format(subject=subject, body=body)
        message = HumanMessage(content=prompt)

        response = structured_llm.invoke([message])
        result = {
            "sentiment": response.sentiment,
            "urgency": response.urgency,
            "frustration_level": response.frustration_level,
            "key_concerns": response.key_concerns,
        }

        logger.info(f"Sentiment analysis: {response.sentiment}")
        return result

    def assess_priority(
        self,
        subject: str,
        body: str,
        category: str,
        sentiment: str,
        urgency: str,
    ) -> dict:
        """Assess priority and escalation needs.

        Args:
            subject: Email subject line
            body: Email body content
            category: Email classification
            sentiment: Sentiment analysis result
            urgency: Urgency level

        Returns:
            Dictionary with priority_level, requires_human_review, reason
        """
        from src.prompts import PRIORITY_ASSESSMENT_PROMPT

        # Create structured LLM
        structured_llm = self.llm.with_structured_output(PriorityOutput)

        prompt = PRIORITY_ASSESSMENT_PROMPT.format(
            subject=subject,
            body=body,
            category=category,
            sentiment=sentiment,
            urgency=urgency,
        )
        message = HumanMessage(content=prompt)

        response = structured_llm.invoke([message])
        result = {
            "priority_level": response.priority_level,
            "requires_human_review": response.requires_human_review,
            "reason": response.reason,
        }

        logger.info(f"Priority assessed: {response.priority_level}")
        return result

    def retrieve_knowledge_queries(
        self, subject: str, body: str, category: str
    ) -> list[str]:
        """Generate knowledge base retrieval queries.

        Args:
            subject: Email subject line
            body: Email body content
            category: Email classification

        Returns:
            List of 3-5 search queries
        """
        from src.prompts import KNOWLEDGE_RETRIEVAL_PROMPT

        # Create structured LLM
        structured_llm = self.llm.with_structured_output(KnowledgeQueryOutput)

        prompt = KNOWLEDGE_RETRIEVAL_PROMPT.format(
            subject=subject,
            body=body,
            category=category,
        )
        message = HumanMessage(content=prompt)

        response = structured_llm.invoke([message])
        queries = response.queries

        logger.info(f"Generated {len(queries)} knowledge queries")
        return queries
