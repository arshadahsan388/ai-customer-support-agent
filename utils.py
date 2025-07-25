"""
Utility functions for the Support Agent system.

This module provides logging, escalation, and other utility functions
used throughout the support ticket processing pipeline.
"""

import csv
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional
from config import SYSTEM_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('support_agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_escalation(
    ticket_id: str,
    subject: str,
    description: str,
    reason: str,
    category: Optional[str] = None
) -> None:
    """
    Log an escalated ticket to the escalation CSV file.
    
    Args:
        ticket_id: Unique identifier for the ticket
        subject: Subject line of the ticket
        description: Description of the issue
        reason: Reason for escalation
        category: Category of the ticket (optional)
    """
    escalation_log_path = SYSTEM_CONFIG["escalation_log_path"]
    
    # Check if file exists and has headers
    file_exists = os.path.exists(escalation_log_path)
    
    try:
        with open(escalation_log_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'timestamp', 'ticket_id', 'subject', 'description', 
                'category', 'escalation_reason'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists or os.path.getsize(escalation_log_path) == 0:
                writer.writeheader()
            
            # Write escalation record
            writer.writerow({
                'timestamp': datetime.now().isoformat(),
                'ticket_id': ticket_id,
                'subject': subject,
                'description': description,
                'category': category or 'Unknown',
                'escalation_reason': reason
            })
            
        logger.info(f"Escalated ticket {ticket_id}: {reason}")
        
    except Exception as e:
        logger.error(f"Failed to log escalation for ticket {ticket_id}: {str(e)}")

def generate_ticket_id() -> str:
    """
    Generate a unique ticket ID based on timestamp.
    
    Returns:
        str: Unique ticket identifier
    """
    return f"TICKET_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]}"

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input by removing dangerous characters and limiting length.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Remove potential injection characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length] + "..."
        logger.warning(f"Input truncated to {max_length} characters")
    
    return text.strip()

def calculate_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate a simple similarity score between two texts.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        float: Similarity score between 0 and 1
    """
    import difflib
    return difflib.SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def is_escalation_needed(state: Dict[str, Any]) -> tuple[bool, str]:
    """
    Determine if a ticket needs escalation based on current state.
    
    Args:
        state: Current state of the support ticket
        
    Returns:
        tuple[bool, str]: (needs_escalation, reason)
    """
    tries = state.get("tries", 0)
    max_tries = SYSTEM_CONFIG["max_retry_attempts"]
    
    # Escalate if max attempts reached
    if tries >= max_tries:
        return True, f"Maximum retry attempts ({max_tries}) exceeded"
    
    # Escalate if no answer could be generated
    if not state.get("answer") or state.get("answer") == "":
        return True, "No suitable answer could be generated"
    
    # Escalate if answer indicates escalation is needed
    answer = state.get("answer", "").lower()
    escalation_keywords = [
        "escalate", "human agent", "specialist", "manager", 
        "cannot help", "unable to resolve", "complex issue"
    ]
    
    if any(keyword in answer for keyword in escalation_keywords):
        return True, "AI agent recommended human escalation"
    
    return False, ""
