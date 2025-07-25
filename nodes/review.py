"""
Quality review node for the Support Agent workflow.

This module handles the automatic quality assessment of generated responses
to ensure they meet professional standards before being sent to customers.
"""

import logging
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GEMINI_API_KEY, MODEL_CONFIG

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model=MODEL_CONFIG["model_name"],
    google_api_key=GEMINI_API_KEY,
    temperature=0.1  # Lower temperature for more consistent review decisions
)

# Quality review prompt template
REVIEW_PROMPT = PromptTemplate.from_template("""
You are a quality assurance reviewer for customer support responses. 
Evaluate the following response based on these criteria:

Quality Criteria:
1. CLARITY: Is the response clear and easy to understand?
2. COMPLETENESS: Does it address the customer's issue comprehensively?
3. PROFESSIONALISM: Is the tone professional and appropriate?
4. ACCURACY: Does the information appear correct and helpful?
5. ACTION_ORIENTED: Does it provide clear next steps?

Customer Issue:
Subject: {subject}
Description: {description}
Category: {category}

Support Response to Review:
{answer}

Based on your evaluation, respond with ONLY one of these decisions:
- approve: Response meets all quality standards
- revise: Response needs improvement before sending

Decision:
""")

def review_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Review the quality of a generated support response.
    
    This node uses AI to evaluate whether a support response meets
    quality standards for clarity, completeness, professionalism,
    and helpfulness before it's sent to the customer.
    
    Args:
        state: Current workflow state containing the response to review
        
    Returns:
        Dict[str, Any]: Updated state with review decision
    """
    try:
        # Extract response and context for review
        answer = state.get("answer", "")
        subject = state.get("subject", "")
        description = state.get("description", "")
        category = state.get("category", "General")
        
        # Skip review if no answer to review
        if not answer:
            logger.warning("No answer provided for review")
            return {
                **state,
                "review_decision": "revise",
                "review_passed": False,
                "review_reason": "No answer to review"
            }
        
        # Skip review for escalated tickets
        if state.get("escalated", False):
            logger.info("Skipping review for escalated ticket")
            return {
                **state,
                "review_decision": "approve",
                "review_passed": True,
                "review_reason": "Escalated ticket - no review needed"
            }
        
        logger.info("Reviewing response quality...")
        
        # Format the review prompt
        formatted_prompt = REVIEW_PROMPT.format(
            subject=subject,
            description=description,
            category=category,
            answer=answer
        )
        
        # Get review decision from AI
        response = llm.invoke(formatted_prompt)
        review_decision = response.content.strip().lower()
        
        # Validate and normalize review decision
        if "approve" in review_decision:
            decision = "approve"
            passed = True
            reason = "Response meets quality standards"
        elif "revise" in review_decision:
            decision = "revise"
            passed = False
            reason = "Response needs improvement"
        else:
            # Default to revision if decision is unclear
            logger.warning(f"Unclear review decision: {review_decision}")
            decision = "revise"
            passed = False
            reason = f"Unclear review decision: {review_decision}"
        
        logger.info(f"Review decision: {decision}")
        
        return {
            **state,
            "review_decision": decision,
            "review_passed": passed,
            "review_reason": reason
        }
        
    except Exception as e:
        logger.error(f"Review process failed: {str(e)}")
        # Default to requiring revision if review fails
        return {
            **state,
            "review_decision": "revise",
            "review_passed": False,
            "review_reason": f"Review error: {str(e)}"
        }

def _perform_manual_quality_check(answer: str) -> tuple[bool, str]:
    """
    Perform basic manual quality checks on the response.
    
    Args:
        answer: The response text to check
        
    Returns:
        tuple[bool, str]: (passes_check, reason)
    """
    # Check minimum length
    if len(answer.strip()) < 20:
        return False, "Response too short"
    
    # Check for placeholder text
    placeholders = ["[placeholder]", "TODO", "FIXME", "XXX"]
    if any(placeholder in answer.upper() for placeholder in placeholders):
        return False, "Contains placeholder text"
    
    # Check for common error patterns
    error_patterns = ["error:", "exception:", "failed to", "null", "undefined"]
    if any(pattern in answer.lower() for pattern in error_patterns):
        return False, "Contains error indicators"
    
    # Check for professional language (basic check)
    unprofessional_words = ["stupid", "dumb", "ridiculous", "annoying"]
    if any(word in answer.lower() for word in unprofessional_words):
        return False, "Contains unprofessional language"
    
    return True, "Passes basic quality checks"

