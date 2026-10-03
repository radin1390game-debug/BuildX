import logging
from typing import TypedDict, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from models import LeadAnalysis
from config import Config

class LeadState(TypedDict):
    raw_message: str
    product_context: str
    api_key: Optional[str]
    analysis: Optional[Dict[str, Any]]
    error: Optional[str]

def analyze_node(state: LeadState) -> Dict[str, Any]:
    try:
        api_key = Config.get_api_key(state.get("api_key"))
        
        llm = ChatGroq(
            model=Config.DEFAULT_MODEL,
            temperature=Config.TEMPERATURE,
            groq_api_key=api_key,
            max_retries=2
        )
        
        structured_llm = llm.with_structured_output(LeadAnalysis)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an elite Sales Development Representative (SDR) and Market Intelligence Agent. "
             "Analyze the target community message against the provided product context. "
             "Identify buying intent, learning requests, or pain points. "
             "Return precise structured evaluation. Language: Persian."),
            ("user", "Product Context:\n{product_context}\n\nUser Message:\n{raw_message}")
        ])
        
        chain = prompt | structured_llm
        result = chain.invoke({
            "product_context": state["product_context"],
            "raw_message": state["raw_message"]
        })
        
        return {"analysis": result.model_dump(), "error": None}

    except Exception as e:
        return {
            "analysis": {
                "is_potential_lead": False,
                "relevance_score": 0,
                "reasoning": f"Error: {str(e)}",
                "suggested_reply": ""
            },
            "error": str(e)
        }

workflow = StateGraph(LeadState)
workflow.add_node("analyzer", analyze_node)
workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", END)

lead_finder_agent = workflow.compile()

def run_lead_finder(raw_message: str, product_context: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    initial_state: LeadState = {
        "raw_message": raw_message,
        "product_context": product_context,
        "api_key": api_key,
        "analysis": None,
        "error": None
    }
    result = lead_finder_agent.invoke(initial_state)
    return result.get("analysis", {})