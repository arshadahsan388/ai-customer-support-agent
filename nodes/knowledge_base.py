"""
Knowledge base module for the Support Agent system.

This module contains the predefined knowledge base with common support questions
and their corresponding answers. It provides functions to search and retrieve
relevant information for customer inquiries.
"""

from typing import List, Dict, Optional

# Knowledge base containing common support questions and answers
KNOWLEDGE_BASE = [
    {
        "id": "billing_001",
        "category": "Billing",
        "question": "I was charged twice",
        "keywords": ["charged twice", "double charge", "duplicate payment", "paid twice", "billed twice", "paid thrice"],
        "answer": "Sorry for the inconvenience. Please share your transaction ID, and we'll refund the extra charge within 3-5 business days."
    },
    {
        "id": "billing_002", 
        "category": "Billing",
        "question": "I paid for premium but it still shows free account",
        "keywords": ["premium not working", "upgrade not working", "paid but still free", "premium not activated"],
        "answer": "Thank you for your payment. Please log out and log back in. If the issue continues after 10 minutes, contact our billing support at billing@example.com."
    },
    {
        "id": "billing_003",
        "category": "Billing", 
        "question": "Payment not working",
        "keywords": ["payment failed", "card declined", "payment error", "can't pay", "payment not working"],
        "answer": "Please verify your payment information and try again. If the issue persists, try a different payment method or contact billing support at billing@example.com."
    },
    {
        "id": "technical_001",
        "category": "Technical",
        "question": "How do I reset my password?",
        "keywords": ["reset password", "forgot password", "password reset", "can't login", "password help"],
        "answer": "Click on 'Forgot Password' at the login page and follow the steps in your email. If you don't receive the email, check your spam folder."
    },
    {
        "id": "technical_002",
        "category": "Technical", 
        "question": "Why is my internet slow?",
        "keywords": ["slow internet", "connection slow", "slow speed", "internet issues", "connectivity problems"],
        "answer": "Please restart your router and modem. Wait 30 seconds before plugging them back in. If the issue persists, contact technical support."
    },
    {
        "id": "security_001",
        "category": "Security",
        "question": "Is my account secure?",
        "keywords": ["account security", "data safe", "privacy", "secure account", "safety"],
        "answer": "Yes, we use industry-standard encryption and security practices. Enable two-factor authentication for additional security."
    },
    {
        "id": "security_002",
        "category": "Security",
        "question": "I think my account was hacked",
        "keywords": ["account hacked", "unauthorized access", "suspicious activity", "security breach", "compromised account"],
        "answer": "Please change your password immediately and enable two-factor authentication. Contact our security team at security@example.com for further assistance."
    }
]

def get_knowledge_base() -> List[Dict[str, str]]:
    """
    Get the complete knowledge base.
    
    Returns:
        List[Dict[str, str]]: List of knowledge base entries
    """
    return KNOWLEDGE_BASE.copy()

def search_by_category(category: str) -> List[Dict[str, str]]:
    """
    Search knowledge base by category.
    
    Args:
        category: The category to search for
        
    Returns:
        List[Dict[str, str]]: List of matching knowledge base entries
    """
    return [item for item in KNOWLEDGE_BASE if item["category"].lower() == category.lower()]

def search_by_keywords(query: str) -> List[Dict[str, str]]:
    """
    Search knowledge base by keywords in the query.
    
    Args:
        query: The search query
        
    Returns:
        List[Dict[str, str]]: List of matching knowledge base entries
    """
    query_lower = query.lower()
    matches = []
    
    for item in KNOWLEDGE_BASE:
        # Check if any keywords match the query
        for keyword in item["keywords"]:
            if keyword.lower() in query_lower:
                matches.append(item)
                break
    
    return matches

def get_answer_by_id(answer_id: str) -> Optional[str]:
    """
    Get an answer by its ID.
    
    Args:
        answer_id: The ID of the knowledge base entry
        
    Returns:
        Optional[str]: The answer if found, None otherwise
    """
    for item in KNOWLEDGE_BASE:
        if item["id"] == answer_id:
            return item["answer"]
    return None

# Legacy support for the old knowledge_base variable
knowledge_base = [{"question": item["question"], "answer": item["answer"]} for item in KNOWLEDGE_BASE]
