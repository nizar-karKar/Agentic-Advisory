import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "mock-key")

from agents.researcher_agent import researcher_agent
from schemas.structure_output_classes import GraphState

def test_researcher_agent_returns_string():
    import agents.researcher_agent
    
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Research findings: 1. Cost is low. 2. Speed is high."
    
    original_llm = agents.researcher_agent.llm
    agents.researcher_agent.llm = mock_llm
    
    try:
        state: GraphState = {
            "question": "Test Question",
            "plan": "Test Plan",
            "research_notes": [],
            "draft": None,
            "critique": None,
            "iteration": 0,
            "max_iterations": 2,
        }
        
        RESEARCHER_SYSTEM = "You are the Researcher agent."
        result = researcher_agent(state, RESEARCHER_SYSTEM)
        
        assert isinstance(result, str)
        assert "Cost is low" in result
        
        mock_llm.invoke.assert_called_once()
    finally:
        agents.researcher_agent.llm = original_llm

if __name__ == "__main__":
    pytest.main([__file__])
