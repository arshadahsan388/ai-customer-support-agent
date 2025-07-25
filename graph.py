

"""
LangGraph workflow definition for the Support Agent system.

This module defines the complete workflow graph that orchestrates the
support ticket processing pipeline, including classification, retrieval,
AI response generation, quality review, and escalation handling.
"""

import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END

# Import all workflow nodes
from nodes.classify import classify_node
from nodes.retrieve import retrieve_node
from nodes.auto_agent import auto_agent_node
from nodes.review import review_node
from nodes.should_continue import should_continue_node

from state import SupportState, create_initial_state, validate_state
from utils import log_escalation, generate_ticket_id

# Configure logging
logger = logging.getLogger(__name__)

def create_graph() -> StateGraph:
    """
    Create and configure the LangGraph workflow for support ticket processing.
    
    The workflow follows this sequence:
    1. CLASSIFY: Categorize the incoming support ticket
    2. RETRIEVE: Search knowledge base for relevant solutions
    3. AUTO_AGENT: Generate AI-powered responses if needed
    4. REVIEW: Quality check the generated response
    5. DECISION: Continue for improvements or end workflow
    
    Returns:
        StateGraph: Compiled workflow graph ready for execution
    """
    logger.info("Creating support agent workflow graph...")
    
    # Initialize the state graph with our state type
    builder = StateGraph(dict)
    
    # Add all processing nodes to the graph
    builder.add_node("classify", classify_node)
    builder.add_node("retrieve", retrieve_node) 
    builder.add_node("auto_agent", auto_agent_node)
    builder.add_node("review", review_node)
    builder.add_node("check", should_continue_node)
    
    # Define the workflow entry point
    builder.set_entry_point("classify")
    
    # Define the linear workflow edges
    builder.add_edge("classify", "retrieve")
    builder.add_edge("retrieve", "auto_agent") 
    builder.add_edge("auto_agent", "review")
    
    # Add conditional routing based on review results
    builder.add_conditional_edges(
        "review",                    # Source node
        should_continue_node,        # Decision function
        {
            "continue": "retrieve",  # Retry from knowledge base search
            "end": END              # Complete the workflow
        }
    )
    
    logger.info("Workflow graph created successfully")
    return builder.compile()

def run_support_workflow(
    subject: str, 
    description: str,
    debug: bool = False
) -> Dict[str, Any]:
    """
    Execute the complete support ticket workflow.
    
    This is a convenience function that handles the full lifecycle of
    a support ticket from initial input to final response generation.
    
    Args:
        subject: Subject line of the support ticket
        description: Detailed description of the customer's issue
        debug: Whether to include debug information in the output
        
    Returns:
        Dict[str, Any]: Final workflow state with response and metadata
        
    Raises:
        ValueError: If input validation fails
        Exception: If workflow execution fails
    """
    try:
        # Validate inputs
        if not subject.strip() and not description.strip():
            raise ValueError("Either subject or description must be provided")
        
        # Create initial state
        initial_state = create_initial_state(subject, description)
        if not validate_state(initial_state):
            raise ValueError("Invalid initial state created")
        
        # Generate ticket ID for tracking
        ticket_id = generate_ticket_id()
        initial_state["ticket_id"] = ticket_id
        
        logger.info(f"Starting workflow for ticket {ticket_id}: {subject[:50]}...")
        
        # Create and execute the workflow
        app = create_graph()
        final_state = app.invoke(initial_state)
        
        # Log completion
        if final_state.get("escalated"):
            logger.info(f"Ticket {ticket_id} escalated: {final_state.get('escalation_reason')}")
        else:
            logger.info(f"Ticket {ticket_id} completed successfully")
        
        # Prepare response
        response = {
            "ticket_id": ticket_id,
            "answer": final_state.get("answer", "No response generated"),
            "category": final_state.get("category", "Unknown"),
            "escalated": final_state.get("escalated", False),
            "attempts": final_state.get("tries", 0)
        }
        
        # Add debug information if requested
        if debug:
            response["debug_info"] = {
                "full_state": final_state,
                "kb_match_id": final_state.get("kb_match_id"),
                "ai_generated": final_state.get("ai_generated", False),
                "review_passed": final_state.get("review_passed", False),
                "escalation_reason": final_state.get("escalation_reason")
            }
        
        return response
        
    except Exception as e:
        logger.error(f"Workflow execution failed: {str(e)}")
        raise

def validate_workflow_health() -> Dict[str, bool]:
    """
    Validate that all components of the workflow are functioning properly.
    
    Returns:
        Dict[str, bool]: Health check results for each component
    """
    health_status = {}
    
    try:
        # Test graph creation
        graph = create_graph()
        health_status["graph_creation"] = True
        
        # Test basic workflow with minimal input
        test_state = {"subject": "test", "description": "test description"}
        result = graph.invoke(test_state)
        health_status["workflow_execution"] = "answer" in result
        
        # Test individual nodes (basic validation)
        health_status["classify_node"] = hasattr(classify_node, "__call__")
        health_status["retrieve_node"] = hasattr(retrieve_node, "__call__")
        health_status["auto_agent_node"] = hasattr(auto_agent_node, "__call__")
        health_status["review_node"] = hasattr(review_node, "__call__")
        health_status["should_continue_node"] = hasattr(should_continue_node, "__call__")
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        health_status["overall"] = False
    
    return health_status
