from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from schemas.structure_output_classes import GraphState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def researcher_agent(state: GraphState,RESEARCHER_SYSTEM:str) -> str:

    resp = llm.invoke([
        SystemMessage(content=RESEARCHER_SYSTEM),
        HumanMessage(content=f"Question:\n{state['question']}\n\nPlan:\n{state['plan']}")
    ]).content

    return resp