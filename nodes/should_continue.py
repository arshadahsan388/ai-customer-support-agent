
"""
Workflow continuation decision node for the Support Agent system.

This module determines whether the support ticket processing should continue
with another iteration or end based on review results and retry limits.
"""

import logging
from typing import Dict, Any
from config import SYSTEM_CONFIG
from utils import log_escalation, generate_ticket_id

# Configure logging
logger = logging.getLogger(__name__)

def should_continue_node(state: Dict[str, Any]) -> str:
    """
    Determine whether to continue processing or end the workflow.
    
    This node makes the critical decision about workflow continuation based on:
    - Review results (whether the response passed quality review)
    - Number of processing attempts made
    - Escalation status
    - Maximum retry limits
    
    Args:
        state: Current workflow state with review and attempt information
        
    Returns:
        str: "continue" to retry processing, "end" to complete workflow
    """
    try:
        # Extract state information
        tries = state.get("tries", 0)
        max_tries = SYSTEM_CONFIG["max_retry_attempts"]
        review_passed = state.get("review_passed", False)
        escalated = state.get("escalated", False)
        review_decision = state.get("review_decision", "")
        
        # Log current attempt information
        logger.info(f"Workflow decision - Tries: {tries}/{max_tries}, "
                   f"Review passed: {review_passed}, Escalated: {escalated}")
        
        # End immediately if ticket is escalated
        if escalated:
            logger.info("Ending workflow - ticket escalated")
            _handle_escalation(state)
            return "end"
        
        # End if review passed (successful completion)
        if review_passed or review_decision == "approve":
            logger.info("Ending workflow - review passed")
            return "end"
        
        # End if maximum attempts reached
        if tries >= max_tries:
            logger.info(f"Ending workflow - maximum attempts ({max_tries}) reached")
            _handle_max_attempts_reached(state)
            return "end"
        
        # Continue for another iteration
        logger.info("Continuing workflow - retrying processing")
        return "continue"
        
    except Exception as e:
        logger.error(f"Error in workflow decision: {str(e)}")
        # Default to ending on error to prevent infinite loops
        return "end"

def _handle_escalation(state: Dict[str, Any]) -> None:
    """
    Handle the escalation process by logging the ticket.
    
    Args:
        state: Current workflow state
    """
    try:
        ticket_id = generate_ticket_id()
        subject = state.get("subject", "Unknown")
        description = state.get("description", "No description")
        category = state.get("category", "General")
        escalation_reason = state.get("escalation_reason", "Unknown reason")
        
        log_escalation(
            ticket_id=ticket_id,
            subject=subject,
            description=description,
            reason=escalation_reason,
            category=category
        )
        
        # Update state with escalation information
        state["ticket_id"] = ticket_id
        state["escalation_logged"] = True
        
        logger.info(f"Escalation logged with ticket ID: {ticket_id}")
        
    except Exception as e:
        logger.error(f"Failed to handle escalation: {str(e)}")

def _handle_max_attempts_reached(state: Dict[str, Any]) -> None:
    """
    Handle the case when maximum retry attempts are reached.
    
    Args:
        state: Current workflow state
    """
    try:
        # Force escalation when max attempts reached
        escalation_reason = f"Maximum processing attempts ({SYSTEM_CONFIG['max_retry_attempts']}) exceeded"
        
        # Update state to indicate escalation
        state.update({
            "escalated": True,
            "escalation_reason": escalation_reason,
            "answer": (
                "We apologize for the delay in resolving your issue. "
                "Your ticket has been escalated to our specialized support team "
                "who will contact you within 24 hours with a resolution."
            )
        })
        
        # Log the escalation
        _handle_escalation(state)
        
        logger.warning(f"Ticket escalated due to max attempts: {escalation_reason}")
        
    except Exception as e:
        logger.error(f"Failed to handle max attempts: {str(e)}")

def get_workflow_status(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a summary of the current workflow status.
    
    Args:
        state: Current workflow state
        
    Returns:
        Dict[str, Any]: Status summary
    """
    return {
        "attempts_made": state.get("tries", 0),
        "max_attempts": SYSTEM_CONFIG["max_retry_attempts"],
        "review_passed": state.get("review_passed", False),
        "escalated": state.get("escalated", False),
        "has_answer": bool(state.get("answer")),
        "ticket_id": state.get("ticket_id"),
        "category": state.get("category", "Unknown")
    }
