"""
Basic tests for the Support Agent system.

Run with: python -m pytest test_support_agent.py -v
"""

import pytest
from unittest.mock import patch, MagicMock

# Import modules to test
from graph import create_graph, run_support_workflow, validate_workflow_health
from nodes.classify import classify_node
from nodes.retrieve import retrieve_node
from nodes.knowledge_base import KNOWLEDGE_BASE, search_by_keywords
from state import create_initial_state, validate_state
from utils import sanitize_input, calculate_similarity_score

class TestSupportAgent:
    """Test suite for the Support Agent system."""
    
    def test_initial_state_creation(self):
        """Test creating initial state."""
        state = create_initial_state("Test subject", "Test description")
        assert state["subject"] == "Test subject"
        assert state["description"] == "Test description"
        assert state["tries"] == 0
        assert state["escalated"] == False
    
    def test_state_validation(self):
        """Test state validation."""
        valid_state = {"subject": "Test", "description": "Test desc"}
        invalid_state = {"subject": "", "description": ""}
        
        assert validate_state(valid_state) == True
        assert validate_state(invalid_state) == False
    
    def test_sanitize_input(self):
        """Test input sanitization."""
        dirty_input = "<script>alert('xss')</script>Test input"
        clean_input = sanitize_input(dirty_input)
        assert "<script>" not in clean_input
        assert "Test input" in clean_input
    
    def test_similarity_calculation(self):
        """Test similarity score calculation."""
        score = calculate_similarity_score("test string", "test string")
        assert score == 1.0
        
        score = calculate_similarity_score("hello world", "goodbye world")
        assert 0 < score < 1
    
    def test_knowledge_base_search(self):
        """Test knowledge base search functionality."""
        # Test keyword search
        results = search_by_keywords("charged twice")
        assert len(results) > 0
        assert any("billing" in result["category"].lower() for result in results)
        
        # Test no match
        results = search_by_keywords("extremely rare issue that should not match")
        assert len(results) == 0
    
    def test_knowledge_base_structure(self):
        """Test knowledge base data structure."""
        assert isinstance(KNOWLEDGE_BASE, list)
        assert len(KNOWLEDGE_BASE) > 0
        
        for entry in KNOWLEDGE_BASE:
            assert "id" in entry
            assert "category" in entry
            assert "question" in entry
            assert "keywords" in entry
            assert "answer" in entry
            assert isinstance(entry["keywords"], list)
    
    @patch('nodes.classify.llm')
    def test_classify_node(self, mock_llm):
        """Test classification node."""
        # Mock the AI response
        mock_response = MagicMock()
        mock_response.content = "Billing"
        mock_llm.invoke.return_value = mock_response
        
        state = {"subject": "Payment issue", "description": "I was charged twice"}
        result = classify_node(state)
        
        assert "category" in result
        assert result["category"] == "Billing"
    
    def test_retrieve_node(self):
        """Test knowledge base retrieval node."""
        state = {"description": "I was charged twice", "category": "Billing"}
        result = retrieve_node(state)
        
        assert "answer" in result
        assert len(result["answer"]) > 0
    
    def test_graph_creation(self):
        """Test graph creation."""
        graph = create_graph()
        assert graph is not None
    
    def test_health_check(self):
        """Test system health validation."""
        health_status = validate_workflow_health()
        assert isinstance(health_status, dict)
        assert "graph_creation" in health_status

class TestWorkflowIntegration:
    """Integration tests for the complete workflow."""
    
    def test_billing_workflow(self):
        """Test complete workflow with billing issue."""
        try:
            result = run_support_workflow(
                subject="Billing problem",
                description="I was charged twice for my subscription"
            )
            
            assert "ticket_id" in result
            assert "answer" in result
            assert "category" in result
            assert len(result["answer"]) > 0
            
        except Exception as e:
            # If API call fails, that's expected in test environment
            assert "API" in str(e) or "key" in str(e)
    
    def test_technical_workflow(self):
        """Test workflow with technical issue."""
        try:
            result = run_support_workflow(
                subject="Password help",
                description="I need to reset my password"
            )
            
            assert "ticket_id" in result
            assert "answer" in result
            assert "category" in result
            
        except Exception as e:
            # If API call fails, that's expected in test environment
            assert "API" in str(e) or "key" in str(e)

if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
