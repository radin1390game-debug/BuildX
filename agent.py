import os
from typing import TypedDict, Optional
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from config import get_groq_api_key

# ---------------------------------------------------------
# 1. تعریف Schema خروجی با Pydantic
# ---------------------------------------------------------
class LeadAnalysisSchema(BaseModel):
    is_potential_lead: bool = Field(
        description="آیا این پیام نشان‌دهنده فرصت فروش (لید) برای خدمت/محصول ما است؟"
    )
    relevance_score: int = Field(
        description="امتیاز ارتباط پیام با خدمت/محصول از 0 تا 100"
    )
    reasoning: str = Field(
        description="تحلیل منطقی و دقیق علت تأیید یا رد پیام"
    )
    suggested_reply: Optional[str] = Field(
        default="",
        description="پاسخ حرفه‌ای و شخصی‌‌سازی‌شده به مشتری (اگر لید مناسب است)"
    )

# ---------------------------------------------------------
# 2. تعریف State برای LangGraph
# ---------------------------------------------------------
class AgentState(TypedDict):
    product_desc: str
    user_msg: str
    api_key: Optional[str]
    result: Optional[dict]
    error: Optional[str]

# فقط مدل‌های رسمی، فعال و آنلاین Groq
CANDIDATE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

# ---------------------------------------------------------
# 3. گره اصلی پردازش
# ---------------------------------------------------------
def analyze_lead_node(state: AgentState) -> AgentState:
    api_key = state.get("api_key") or get_groq_api_key()
    
    if not api_key or not api_key.strip():
        return {
            **state,
            "error": "کلید API معتبر یافت نشد. لطفاً کلید Groq API خود را در کادر مربوطه یا فایل .env وارد کنید."
        }

    last_error = None

    for model_name in CANDIDATE_MODELS:
        try:
            llm = ChatGroq(
                groq_api_key=api_key.strip(),
                model_name=model_name,
                temperature=0.1,
                max_retries=2,
                request_timeout=25.0
            )

            structured_llm = llm.with_structured_output(LeadAnalysisSchema)

            prompt = ChatPromptTemplate.from_messages([
                ("system", """شما یک ایجنت ارزیابی دقیق فرصت‌های فروش (Lead Qualification Agent) هستید.
وظیفه شما بررسی پیام دریافت شده از جوامع آنلاین و تطبیق آن با خدمات/محصول ارائه شده است.

پاسخ شما باید کاملاً فارسی، حرفه‌ای و دقیق باشد.

ورودی‌ها:
- توضیحات محصول/خدمت: {product_desc}
- پیام کاربر/مشتری: {user_msg}
"""),
                ("human", "توضیحات خدمت:\n{product_desc}\n\nپیام دریافتی:\n{user_msg}")
            ])

            chain = prompt | structured_llm
            
            response: LeadAnalysisSchema = chain.invoke({
                "product_desc": state["product_desc"],
                "user_msg": state["user_msg"]
            })

            return {
                **state,
                "result": response.model_dump(),
                "error": None
            }

        except Exception as e:
            last_error = str(e)
            continue

    return {
        **state,
        "error": f"خطا در ارتباط با مدل‌های Groq (لطفاً از معتبر بودن API Key مطمئن شوید). جزئیات: {last_error}"
    }

# ---------------------------------------------------------
# 4. ساخت گراف LangGraph
# ---------------------------------------------------------
workflow = StateGraph(AgentState)
workflow.add_node("analyzer", analyze_lead_node)
workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", END)

agent_app = workflow.compile()

# ---------------------------------------------------------
# 5. تابع فراخوانی
# ---------------------------------------------------------
def run_lead_finder(product_desc: str, user_msg: str, custom_api_key: Optional[str] = None) -> dict:
    initial_state: AgentState = {
        "product_desc": product_desc,
        "user_msg": user_msg,
        "api_key": custom_api_key,
        "result": None,
        "error": None
    }

    final_state = agent_app.invoke(initial_state)

    if final_state.get("error"):
        raise RuntimeError(final_state["error"])

    return final_state["result"]
