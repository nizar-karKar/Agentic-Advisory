import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "mock-key")

from agents.navigator_agent import navigator_agent

def test_navigator_agent_returns_dict():
    # Since navigator_agent creates the Agent inside the function, 
    # we need to patch the Agent class in the module.
    
    with patch("agents.navigator_agent.Agent") as MockAgent:
        mock_agent_instance = MockAgent.return_value
        
        # Mock response.content.model_dump()
        mock_response = MagicMock()
        mock_response.content.model_dump.return_value = {
            "top_trend_ai_topics": {
                "Topic 1": "Description 1",
                "Topic 2": "Description 2",
                "Topic 3": "Description 3",
                "Topic 4": "Description 4",
                "Topic 5": "Description 5"
            }
        }
        mock_agent_instance.run.return_value = mock_response
        
        result = navigator_agent()
        
        assert isinstance(result, dict)
        assert "top_trend_ai_topics" in result
        assert len(result["top_trend_ai_topics"]) == 5
        
        MockAgent.assert_called_once()
        mock_agent_instance.run.assert_called_once()

if __name__ == "__main__":
    pytest.main([__file__])
