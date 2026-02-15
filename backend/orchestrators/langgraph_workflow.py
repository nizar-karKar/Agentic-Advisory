import os
from dotenv import load_dotenv

# Load environment variables FIRST, before importing agents
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "agentic-advisory-project")
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Now import agents - they can safely use the API key
from agents.planner_agent import planner_agent
from agents.researcher_agent import researcher_agent
from agents.writer_agent import writer_agent
from agents.critic_agent import critic_agent
from schemas.structure_output_classes import GraphState
from langchain_core.messages import HumanMessage, SystemMessage

from langgraph.graph import StateGraph,END,START
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any, Optional, TypedDict, Literal

print("Tracing:", os.environ["LANGCHAIN_TRACING_V2"])
print("Project:", os.environ["LANGCHAIN_PROJECT"])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# Agent nodes (Planner, Researcher, Writer, Critic, finalizer)

PLANNER_SYSTEM = """You are the Planner agent.
Create a concise plan with steps, key risks, and final output headings.
Return valid JSON matching the schema.
"""

RESEARCHER_SYSTEM = """You are the Researcher agent.
You do NOT browse the web. You reason from general knowledge.
Produce bullet research notes covering: cost, speed, privacy, reliability, compliance, vendor lock-in, iteration speed, support.
Keep it practical for startups.
"""

WRITER_SYSTEM = """You are the Writer agent.
Write a structured answer using the plan headings.
Use the research notes.
Be specific, actionable, and include a clear recommendation plus risks.
"""

CRITIC_SYSTEM = """You are the Critic agent.
Review the draft for:
- missing points
- weak reasoning
- overconfidence
- risky claims
Return JSON matching the schema.
"""

FUNALIZER_SYSTEM = """You are the finalizer agent.
Given the plan + research notes + (optional) critique, produce the FINAL answer.
If critique exists, incorporate fixes.
Output must be polished and concise with headings and a confidence score.
"""

def planner_node(state: GraphState) -> GraphState:
    plan_obj = planner_agent(state,PLANNER_SYSTEM)
    state["plan"] = plan_obj.model_dump()
    return state

def researcher_node(state: GraphState) -> GraphState:
    resp = researcher_agent(state,RESEARCHER_SYSTEM)
    # store as notes (simple split)
    notes = [line.strip("- ").strip() for line in resp.split("\n") if line.strip()]
    state["research_notes"] = notes
    return state

def writer_node(state: GraphState) -> GraphState:
    resp = writer_agent(state,WRITER_SYSTEM)
    state["draft"] = resp
    return state

def critic_node(state: GraphState) -> GraphState:
    resp = critic_agent(state,CRITIC_SYSTEM)
    state["critique"] = resp.model_dump()
    state["iteration"] += 1
    return state


def finalizer_node(state: GraphState) -> GraphState:
    resp = llm.invoke([
        SystemMessage(content=FUNALIZER_SYSTEM),
        HumanMessage(content=f"""
Question:
{state['question']}

Plan:
{state['plan']}

Research notes:
{state['research_notes']}

Critique (if any):
{state.get('critique')}

Current draft (if any):
{state.get('draft')}
""")
    ]).content

    state["draft"] = resp
    return state


def should_revise(state: GraphState) -> Literal["revise", "finalize"]:
    score = state["critique"]["score"]

    if state["iteration"] >= state["max_iterations"]:
        return "finalize"

    if score < 80:
        return "revise"

    return "finalize"

def build_workflow():
    workflow = StateGraph(GraphState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)
    workflow.add_node("finalizer", finalizer_node)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "critic")

    # conditional edge to loop or finalize
    workflow.add_conditional_edges(
        "critic",
        should_revise,
        {
            "revise": "writer",
            "finalize": "finalizer",
        }
    )
    workflow.add_edge("finalizer", END)

    return workflow.compile()


def visualize_graph():
    app = build_workflow()
    try:
        from IPython.display import Image, display
        display(Image(app.get_graph().draw_mermaid_png()))
    except Exception as e:
        print("Graph visualization skipped:", e)


app=build_workflow()
question = "Should a startup use open-source LLMs or closed models in 2026? Consider cost, speed, privacy, and reliability."
initial_state: GraphState = {
    "question": question,
    "plan": None,
    "research_notes": [],
    "draft": None,
    "critique": None,
    "iteration": 0,
    "max_iterations": 2,
}


def run_workflow(
    question: str,
    max_iterations: int = 2,
) -> dict:
    """
    Entry point for executing the LangGraph workflow.
    Safe for API usage.
    """
    graph_app = build_workflow()
    initial_state: GraphState = {
        "question": question,
        "plan": None,
        "research_notes": [],
        "draft": None,
        "critique": None,
        "iteration": 0,
        "max_iterations": max_iterations,
    }

    result = graph_app.invoke(initial_state)

    return {
        "final_answer": result["draft"],
        "iterations": result["iteration"],
        "critique": result.get("critique"),
    }

