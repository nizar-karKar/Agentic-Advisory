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

from agents.planner_agent import planner_agent
from schemas.structure_output_classes import GraphState, Plan

def test_planner_agent_returns_plan():
    import agents.planner_agent
    
    # Mock llm.with_structured_output(Plan).invoke(...)
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured
    
    expected_plan = Plan(steps=["Step 1", "Step 2"])
    mock_structured.invoke.return_value = expected_plan
    
    original_llm = agents.planner_agent.llm
    agents.planner_agent.llm = mock_llm
    
    try:
        state: GraphState = {
            "question": "Should I use open source LLMs?",
            "plan": None,
            "research_notes": [],
            "draft": None,
            "critique": None,
            "iteration": 0,
            "max_iterations": 2,
        }
        
        PLANNER_SYSTEM = "You are the Planner agent."
        result = planner_agent(state, PLANNER_SYSTEM)
        
        assert isinstance(result, Plan)
        assert result.steps == ["Step 1", "Step 2"]
        
        # Verify LLM was called correctly
        mock_llm.with_structured_output.assert_called_once_with(Plan)
        mock_structured.invoke.assert_called_once()
        
    finally:
        agents.planner_agent.llm = original_llm

if __name__ == "__main__":
    pytest.main([__file__])
