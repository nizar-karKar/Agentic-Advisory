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

from agents.critic_agent import critic_agent
from schemas.structure_output_classes import GraphState, Critique

def test_critic_agent_returns_critique():
    import agents.critic_agent
    
    mock_llm = MagicMock()
    mock_structured = MagicMock()
    mock_llm.with_structured_output.return_value = mock_structured
    
    expected_critique = Critique(
        score=85, 
        issues=["Good work, but add more details."],
        missing_points=["Deep dive into specific model architectures", "Cost analysis"],
        hallucination_risk=["Claim about 2026 usage stats needs citation"],
        fix_instructions=["Add a section comparing API costs", "Cite the usage statistics source"]
    )
    mock_structured.invoke.return_value = expected_critique
    
    original_llm = agents.critic_agent.llm
    agents.critic_agent.llm = mock_llm
    
    try:
        state: GraphState = {
            "question": "Test Question",
            "plan": "Test Plan",
            "research_notes": ["Note 1"],
            "draft": "Initial draft",
            "critique": None,
            "iteration": 0,
            "max_iterations": 2,
        }
        
        CRITIC_SYSTEM = "You are the Critic agent."
        result = critic_agent(state, CRITIC_SYSTEM)
        
        assert isinstance(result, Critique)
        assert result.score == 85
        assert result.issues == ["Good work, but add more details."]
        assert result.missing_points == ["Deep dive into specific model architectures", "Cost analysis"]
        assert result.hallucination_risk == ["Claim about 2026 usage stats needs citation"]
        assert result.fix_instructions == ["Add a section comparing API costs", "Cite the usage statistics source"]
        
        mock_llm.with_structured_output.assert_called_once_with(Critique)
        mock_structured.invoke.assert_called_once()
    finally:
        agents.critic_agent.llm = original_llm

if __name__ == "__main__":
    pytest.main([__file__])
