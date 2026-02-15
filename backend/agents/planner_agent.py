import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.structure_output_classes import GraphState,Plan
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils.cost_tracker import CostTracker

import os 
from dotenv import load_dotenv
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).bind(response_format={"type": "json_object"})
def planner_agent(state: GraphState,PLANNER_SYSTEM:str) -> Plan:
    structured_planner = llm.with_structured_output(Plan)
    plan_obj = structured_planner.invoke([
        SystemMessage(content=PLANNER_SYSTEM),
        HumanMessage(content=state["question"])
    ])
    return plan_obj 

