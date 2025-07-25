

"""
Information retrieval node for the Support Agent workflow.

This module handles retrieving relevant answers from the knowledge base
using semantic similarity matching and keyword-based search.
"""

import logging
from typing import Dict, Any, Optional, List
import difflib

from .knowledge_base import KNOWLEDGE_BASE, search_by_keywords, search_by_category
from config import SYSTEM_CONFIG
from utils import calculate_similarity_score, sanitize_input

# Configure logging
logger = logging.getLogger(__name__)

def retrieve_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve relevant information from the knowledge base.
    
    This node searches the knowledge base for answers that match the user's
    query using multiple search strategies: keyword matching, similarity
    matching, and category-based filtering.
    
    Args:
        state: Current workflow state containing user query information
        
    Returns:
        Dict[str, Any]: Updated state with retrieved answer
    """
    try:
        # Extract and sanitize user input
        user_description = sanitize_input(state.get("description", ""))
        user_category = state.get("category", "")
        
        if not user_description:
            logger.warning("No description provided for knowledge base search")
            return _create_fallback_response(state, "No description provided")
        
        logger.info(f"Searching knowledge base for: {user_description[:100]}...")
        
        # Strategy 1: Search by keywords first (most precise)
        keyword_matches = search_by_keywords(user_description)
        if keyword_matches:
            best_match = _find_best_match(user_description, keyword_matches)
            if best_match:
                logger.info(f"Found keyword match: {best_match['id']}")
                return _create_success_response(state, best_match)
        
        # Strategy 2: Search by category if available
        if user_category:
            category_matches = search_by_category(user_category)
            if category_matches:
                best_match = _find_best_match(user_description, category_matches)
                if best_match:
                    logger.info(f"Found category match: {best_match['id']}")
                    return _create_success_response(state, best_match)
        
        # Strategy 3: Fallback to similarity search across all questions
        similarity_match = _find_similarity_match(user_description)
        if similarity_match:
            logger.info(f"Found similarity match: {similarity_match['id']}")
            return _create_success_response(state, similarity_match)
        
        # No matches found
        logger.info("No relevant knowledge base entries found")
        return _create_fallback_response(state, "No matching solution found")
        
    except Exception as e:
        logger.error(f"Knowledge base retrieval failed: {str(e)}")
        return _create_fallback_response(state, f"Search error: {str(e)}")

def _find_best_match(query: str, matches: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    Find the best match from a list of potential matches using similarity scoring.
    
    Args:
        query: The user's query
        matches: List of potential knowledge base matches
        
    Returns:
        Optional[Dict[str, Any]]: Best matching entry or None
    """
    if not matches:
        return None
    
    best_match = None
    best_score = 0
    threshold = SYSTEM_CONFIG["similarity_threshold"]
    
    for match in matches:
        # Calculate similarity with question and keywords
        question_score = calculate_similarity_score(query, match["question"])
        keyword_score = max([
            calculate_similarity_score(query, keyword) 
            for keyword in match["keywords"]
        ], default=0)
        
        # Use the higher of the two scores
        score = max(question_score, keyword_score)
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = match
    
    logger.debug(f"Best match score: {best_score}")
    return best_match

def _find_similarity_match(query: str) -> Optional[Dict[str, Any]]:
    """
    Find the most similar question in the entire knowledge base.
    
    Args:
        query: The user's query
        
    Returns:
        Optional[Dict[str, Any]]: Best matching entry or None
    """
    questions = [item["question"] for item in KNOWLEDGE_BASE]
    threshold = SYSTEM_CONFIG["similarity_threshold"]
    
    # Use difflib for backward compatibility
    best_matches = difflib.get_close_matches(
        query, questions, n=1, cutoff=threshold
    )
    
    if best_matches:
        matched_question = best_matches[0]
        for item in KNOWLEDGE_BASE:
            if item["question"] == matched_question:
                return item
    
    return None

def _create_success_response(state: Dict[str, Any], match: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a successful response with the matched answer.
    
    Args:
        state: Current state
        match: Matched knowledge base entry
        
    Returns:
        Dict[str, Any]: Updated state with answer
    """
    return {
        **state,
        "answer": match["answer"],
        "kb_match_id": match["id"],
        "kb_match_category": match["category"]
    }

def _create_fallback_response(state: Dict[str, Any], reason: str) -> Dict[str, Any]:
    """
    Create a fallback response when no match is found.
    
    Args:
        state: Current state
        reason: Reason for fallback
        
    Returns:
        Dict[str, Any]: Updated state with fallback message
    """
    fallback_message = (
        "I couldn't find a specific solution for your issue in our knowledge base. "
        "Our support team will review your request and get back to you soon. "
        "For urgent matters, please contact support@example.com."
    )
    
    return {
        **state,
        "answer": fallback_message,
        "kb_match_id": None,
        "fallback_reason": reason
    }
    
