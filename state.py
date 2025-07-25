"""
State management for the Support Agent workflow.

This module defines the state structure and provides utility functions
for managing state transitions throughout the support ticket processing pipeline.
"""

from typing import Dict, Any, Optional, TypedDict
from enum import Enum

class SupportCategory(Enum):
    """Enumeration of support ticket categories."""
    BILLING = "Billing"
    TECHNICAL = "Technical"
    SECURITY = "Security"
    GENERAL = "General"

class ReviewDecision(Enum):
    """Enumeration of review decisions."""
    APPROVE = "approve"
    REVISE = "revise"

class WorkflowDecision(Enum):
    """Enumeration of workflow continuation decisions."""
    CONTINUE = "continue"
    END = "end"

class SupportState(TypedDict, total=False):
    """
    TypedDict defining the structure of the support agent state.
    
    Attributes:
        subject: The subject line of the support ticket
        description: Detailed description of the user's issue
        category: Classified category of the support ticket
        answer: Generated or retrieved answer to the user's query
        review_decision: Decision from the review process
        review_passed: Boolean indicating if review was passed
        tries: Number of processing attempts made
        escalated: Boolean indicating if ticket was escalated
        escalation_reason: Reason for escalation if applicable
    """
    subject: str
    description: str
    category: Optional[str]
    answer: Optional[str]
    review_decision: Optional[str]
    review_passed: Optional[bool]
    tries: Optional[int]
    escalated: Optional[bool]
    escalation_reason: Optional[str]

def create_initial_state(subject: str, description: str) -> SupportState:
    """
    Create an initial state for a new support ticket.
    
    Args:
        subject: The subject line of the support ticket
        description: Detailed description of the issue
        
    Returns:
        SupportState: Initial state dictionary
    """
    return SupportState(
        subject=subject.strip(),
        description=description.strip(),
        tries=0,
        escalated=False
    )

def update_state(current_state: SupportState, **updates) -> SupportState:
    """
    Update the current state with new values.
    
    Args:
        current_state: The current state dictionary
        **updates: Key-value pairs to update in the state
        
    Returns:
        SupportState: Updated state dictionary
    """
    new_state = current_state.copy()
    new_state.update(updates)
    return new_state

def validate_state(state: SupportState) -> bool:
    """
    Validate that the state contains required fields.
    
    Args:
        state: The state dictionary to validate
        
    Returns:
        bool: True if state is valid, False otherwise
    """
    required_fields = ["subject", "description"]
    return all(field in state and state[field] for field in required_fields)
