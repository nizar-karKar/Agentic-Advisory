
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from schemas.structure_output_classes import GraphState, Critique

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def critic_agent(state: GraphState,CRITIC_SYSTEM:str) -> Critique:
    
    structured_critic = llm.with_structured_output(Critique)
    critique_obj = structured_critic.invoke([
        SystemMessage(content=CRITIC_SYSTEM),
        HumanMessage(content=f"""
    Question:
    {state['question']}

    Draft:
    {state['draft']}
    """)
    ])


    return critique_obj

