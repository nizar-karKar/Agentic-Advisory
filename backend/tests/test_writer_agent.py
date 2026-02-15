import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "mock-key")

from agents.writer_agent import writer_agent
from schemas.structure_output_classes import GraphState

# -----------------------------
# Test: Writer produces output
# -----------------------------

def test_writer_returns_string():
    # Use a manual mock to avoid Pydantic conflict with patch()
    import agents.writer_agent
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = """# Executive Summary
Open-source models reduce cost.
Closed models increase deployment speed.

## Recommendation
Start closed, migrate later.

Confidence: 90%
"""
    
    original_llm = agents.writer_agent.llm
    agents.writer_agent.llm = mock_llm
    
    try:
        state: GraphState = {
            "question": "Open-source vs closed LLMs?",
            "plan": {"steps": ["Compare cost", "Compare speed"]},
            "research_notes": ["Open-source cheaper", "Closed faster"],
            "draft": None,
            "critique": None,
            "iteration": 0,
            "max_iterations": 2,
        }

        WRITER_SYSTEM = "You are the Writer agent."
        result = writer_agent(state, WRITER_SYSTEM)

        assert isinstance(result, str)
        assert len(result) > 20
        assert "Recommendation" in result
        
        # Verify LLM was called
        mock_llm.invoke.assert_called_once()
    finally:
        # Restore original llm
        agents.writer_agent.llm = original_llm

# -----------------------------
# Test: Writer handles critique
# -----------------------------

def test_writer_with_critique():
    import agents.writer_agent
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Revised content based on critique."
    
    original_llm = agents.writer_agent.llm
    agents.writer_agent.llm = mock_llm
    
    try:
        state: GraphState = {
            "question": "Open-source vs closed LLMs?",
            "plan": {"steps": ["Compare cost"]},
            "research_notes": ["Open-source cheaper"],
            "draft": None,
            "critique": {"score": 60, "issues": ["Missing risks"]},
            "iteration": 1,
            "max_iterations": 2,
        }

        WRITER_SYSTEM = "You are the Writer agent."
        result = writer_agent(state, WRITER_SYSTEM)

        assert isinstance(result, str)
        assert "Revised content" in result
    finally:
        # Restore original llm
        agents.writer_agent.llm = original_llm

if __name__ == "__main__":
    pytest.main([__file__])