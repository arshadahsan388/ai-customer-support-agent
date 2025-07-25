
"""
Classification node for the Support Agent workflow.

This module handles the automatic classification of support tickets into
predefined categories using AI-powered text analysis.
"""

import logging
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_API_KEY, MODEL_CONFIG, SUPPORT_CATEGORIES
from utils import sanitize_input

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model=MODEL_CONFIG["model_name"],
    google_api_key=GEMINI_API_KEY,
    temperature=MODEL_CONFIG["temperature"]
)

# Classification prompt template
CLASSIFICATION_PROMPT = PromptTemplate.from_template("""
You are an expert support ticket classifier for a customer service system.

Your task is to classify the following support ticket into exactly ONE of these categories:
{categories}

Classification Guidelines:
- Billing: Payment issues, subscription problems, refunds, charges, invoicing
- Technical: Software bugs, connectivity issues, feature problems, system errors
- Security: Account access, password issues, data privacy, suspicious activity
- General: Questions, feedback, requests that don't fit other categories

Support Ticket:
Subject: {subject}
Description: {description}

Important: Return ONLY the category name (exactly as listed above). No explanation needed.
""")

def classify_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify a support ticket into a predefined category.
    
    This node uses AI to automatically categorize incoming support tickets
    based on their subject and description. The classification helps route
    tickets to appropriate handlers and retrieve relevant knowledge base entries.
    
    Args:
        state: Current workflow state containing 'subject' and 'description'
        
    Returns:
        Dict[str, Any]: Updated state with 'category' field added
        
    Raises:
        Exception: If classification fails, defaults to 'General' category
    """
    try:
        # Extract and sanitize input
        subject = sanitize_input(state.get("subject", ""))
        description = sanitize_input(state.get("description", ""))
        
        if not subject and not description:
            logger.warning("Empty subject and description provided for classification")
            return {**state, "category": "General"}
        
        # Format the prompt with categories and ticket information
        categories_str = ", ".join(SUPPORT_CATEGORIES)
        formatted_prompt = CLASSIFICATION_PROMPT.format(
            categories=categories_str,
            subject=subject,
            description=description
        )
        
        logger.info(f"Classifying ticket: {subject[:50]}...")
        
        # Get classification from the model
        response = llm.invoke(formatted_prompt)
        category = response.content.strip()
        
        # Validate the returned category
        if category not in SUPPORT_CATEGORIES:
            logger.warning(f"Invalid category returned: {category}. Defaulting to General.")
            category = "General"
        
        logger.info(f"Ticket classified as: {category}")
        
        return {**state, "category": category}
        
    except Exception as e:
        logger.error(f"Classification failed: {str(e)}")
        # Fallback to General category if classification fails
        return {**state, "category": "General"}
