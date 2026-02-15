from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from schemas.structure_output_classes import GraphState

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def writer_agent(state: GraphState,WRITER_SYSTEM:str) -> str:
    resp = llm.invoke([
        SystemMessage(content=WRITER_SYSTEM),
        HumanMessage(content=f"""
        Question:
        {state['question']}

        Plan:
        {state['plan']}

        Research notes:
        {state['research_notes']}

        If critique exists, you may improve the draft accordingly.
        Critique:
        {state.get('critique')}
        """)
            ]).content

    return resp