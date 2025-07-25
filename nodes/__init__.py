"""
Support Agent workflow nodes package.

This package contains all the processing nodes for the support ticket workflow,
including classification, retrieval, response generation, and quality review.
"""

# Import all node functions for easy access
from .classify import classify_node
from .retrieve import retrieve_node
from .auto_agent import auto_agent_node
from .review import review_node
from .should_continue import should_continue_node
from .knowledge_base import KNOWLEDGE_BASE, get_knowledge_base

__all__ = [
    'classify_node',
    'retrieve_node', 
    'auto_agent_node',
    'review_node',
    'should_continue_node',
    'KNOWLEDGE_BASE',
    'get_knowledge_base'
]
