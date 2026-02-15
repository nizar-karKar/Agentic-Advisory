from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List,Dict
import os
from dotenv import load_dotenv
import json

# Load environment variables FIRST, before importing agents
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class WebNavigatorOutput(BaseModel):
    top_trend_ai_topics: Dict[str, str] = Field(description="List of top trend AI topics")

def get_current_month_name():
    return datetime.now().strftime("%B")


def navigator_agent():
    prompt = f"""
    Use DuckDuckGo to search and find the top 5 trending AI topics in {get_current_month_name()} 2026.

    Return:
    - Exactly 5 items
    - Key = topic name
    - Value = short 1-2 sentence description
    """

    agent = Agent(
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGo(search=True, news=False)],
        show_tool_calls=True,
        response_model=WebNavigatorOutput,
        markdown=True,
    )

    response = agent.run(prompt)

    # This already returns structured data
    return response.content.model_dump()


print(navigator_agent())