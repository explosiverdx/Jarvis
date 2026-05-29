"""
Tests for NLP Engine
"""

import pytest
from jarvis.core.nlp_engine import NLPEngine


class TestNLPEngine:
    """Test NLP Engine"""
    
    @pytest.fixture
    def nlp(self):
        """Create NLP engine for testing"""
        return NLPEngine()
    
    def test_initialization(self, nlp):
        """Test NLP engine initialization"""
        assert nlp is not None
        assert nlp.commands is not None
    
    def test_process_greeting(self, nlp):
        """Test processing greeting command"""
        intent, entities = nlp.process("hello")
        assert intent == "greeting"
    
    def test_process_time(self, nlp):
        """Test processing time query"""
        intent, entities = nlp.process("what time is it")
        assert intent == "get_time"
    
    def test_process_unknown(self, nlp):
        """Test processing unknown command"""
        intent, entities = nlp.process("xyzabc")
        assert intent == "unknown"
    
    def test_extract_entities(self, nlp):
        """Test entity extraction"""
        intent, entities = nlp.process("remind me at 2:30 pm")
        assert "time" in entities
    
    def test_get_response(self, nlp):
        """Test getting response for intent"""
        response = nlp.get_response("greeting")
        assert response is not None
        assert len(response) > 0
    
    def test_add_custom_intent(self, nlp):
        """Test adding custom intent"""
        nlp.add_custom_intent(
            "test_intent",
            ["test pattern"],
            ["test response"]
        )
        assert "test_intent" in nlp.commands


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
