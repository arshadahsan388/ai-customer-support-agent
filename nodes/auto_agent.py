"""
Automated agent node for the Support Agent workflow.

This module handles AI-powered response generation when knowledge base
retrieval is insufficient or when additional context is needed.
"""

import logging
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_API_KEY, MODEL_CONFIG
from utils import sanitize_input, is_escalation_needed

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model=MODEL_CONFIG["model_name"],
    google_api_key=GEMINI_API_KEY,
    temperature=MODEL_CONFIG["temperature"]
)

# AI Agent prompt template
AI_AGENT_PROMPT = PromptTemplate.from_template("""
You are a professional AI customer support agent. Your goal is to provide helpful, accurate, and empathetic responses to customer inquiries.

Customer Information:
Subject: {subject}
Description: {description}
Category: {category}

Previous Knowledge Base Response:
{previous_answer}

Instructions:
1. If the previous answer from the knowledge base is adequate, enhance it with additional helpful information
2. If the previous answer is insufficient, provide a comprehensive response based on the customer's issue
3. Be professional, empathetic, and solution-oriented
4. If you cannot resolve the issue, clearly explain the escalation process
5. Always include next steps for the customer

Response Guidelines:
- Keep responses concise but complete (max 200 words)
- Use a friendly but professional tone
- Provide specific actionable steps when possible
- Include relevant contact information if escalation is needed
- Acknowledge the customer's frustration if applicable

Generate a helpful response:
""")

def auto_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an AI-powered response for the customer inquiry.
    
    This node uses advanced language models to create personalized,
    contextual responses based on the customer's issue, category,
    and any previous knowledge base matches.
    
    Args:
        state: Current workflow state with customer information and context
        
    Returns:
        Dict[str, Any]: Updated state with AI-generated response
    """
    try:
        # Extract and sanitize inputs
        subject = sanitize_input(state.get("subject", ""))
        description = sanitize_input(state.get("description", ""))
        category = state.get("category", "General")
        previous_answer = state.get("answer", "No previous answer available")
        
        # Check if escalation is immediately needed
        needs_escalation, escalation_reason = is_escalation_needed(state)
        if needs_escalation:
            logger.info(f"Escalation needed: {escalation_reason}")
            return _create_escalation_response(state, escalation_reason)
        
        logger.info(f"Generating AI response for {category} ticket: {subject[:50]}...")
        
        # Format the prompt with all available context
        formatted_prompt = AI_AGENT_PROMPT.format(
            subject=subject,
            description=description,
            category=category,
            previous_answer=previous_answer
        )
        
        # Generate response using the AI model
        response = llm.invoke(formatted_prompt)
        ai_answer = response.content.strip()
        
        # Validate response quality
        if not ai_answer or len(ai_answer) < 20:
            logger.warning("Generated response is too short or empty")
            return _create_fallback_response(state)
        
        logger.info("AI response generated successfully")
        
        return {
            **state,
            "answer": ai_answer,
            "ai_generated": True,
            "tries": state.get("tries", 0) + 1
        }
        
    except Exception as e:
        logger.error(f"AI agent response generation failed: {str(e)}")
        return _create_fallback_response(state, str(e))

def _create_escalation_response(state: Dict[str, Any], reason: str) -> Dict[str, Any]:
    """
    Create an escalation response when the issue needs human intervention.
    
    Args:
        state: Current state
        reason: Reason for escalation
        
    Returns:
        Dict[str, Any]: Updated state with escalation response
    """
    escalation_response = (
        "Thank you for contacting us. Your inquiry requires specialized attention "
        "from our support team. We've escalated your ticket and a human agent will "
        "contact you within 24 hours. For urgent matters, please call our support "
        "hotline at 1-800-SUPPORT."
    )
    
    return {
        **state,
        "answer": escalation_response,
        "escalated": True,
        "escalation_reason": reason,
        "ai_generated": False
    }

def _create_fallback_response(state: Dict[str, Any], error: str = None) -> Dict[str, Any]:
    """
    Create a fallback response when AI generation fails.
    
    Args:
        state: Current state
        error: Optional error message
        
    Returns:
        Dict[str, Any]: Updated state with fallback response
    """
    fallback_response = (
        "We apologize for the inconvenience. We're experiencing technical difficulties "
        "generating a response for your inquiry. A human support agent will review "
        "your request and respond within 4-6 hours. Thank you for your patience."
    )
    
    return {
        **state,
        "answer": fallback_response,
        "ai_generated": False,
        "generation_error": error,
        "escalated": True,
        "escalation_reason": "AI generation failure"
    }
