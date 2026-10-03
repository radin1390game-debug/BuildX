import os
from typing import TypedDict, Optional
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from config import get_groq_api_key, get_groq_model


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
        description="پاسخ حرفه‌ای و شخصی‌سازی‌شده به مشتری (اگر لید مناسب است)"
    )


class AgentState(TypedDict):
    product_desc: str
    user_msg: str
    api_key: Optional[str]
    result: Optional[dict]
    error: Optional[str]


def analyze_lead_node(state: AgentState) -> AgentState:
    api_key = state.get("api_key") or get_groq_api_key()
    
    if not api_key:
        return {
            **state,
            "error": "کلید API معتبر یافت نشد. لطفاً کلید Groq API را در .env یا ورودی وارد کنید."
        }

    model_name = get_groq_model()

    try:
        # مقداردهی اولیه LLM با تنظیم دمای پایین برای دقت بالا
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0.1
        )

        # اجبار مدل به تولید خروجی دقیقاً طبق ساختار Pydantic
        structured_llm = llm.with_structured_output(LeadAnalysisSchema)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """شما یک ایجنت ارزیابی دقیق فرصت‌های فروش (Lead Qualification Agent) هستید.
وظیفه شما بررسی پیام دریافت شده از جوامع آنلاین و تطبیق آن با خدمات/محصول ارائه شده است.

پاسخ شما باید کاملاً فارسی، حرفه‌ای و دقیق باشد.

ورودی‌ها:
- توضیحات محصول/خدمت: {product_desc}
- پیام کاربر/مشتری: {user_msg}

ارزیابی کنید:
1. آیا پیام یک لید واقعی است؟
2. امتیاز ارتباط (0 تا 100) چقدر است؟
3. استدلال منطقی خود را بنویسید.
4. در صورت لید بودن، یک پاسخ جذاب و حرفه‌ای پیشنهاد دهید.
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
            "result": response.dict(),
            "error": None
        }

    except Exception as e:
        return {
            **state,
            "error": f"خطا در اجرای ایجنت: {str(e)}"
        }


workflow = StateGraph(AgentState)


workflow.add_node("analyzer", analyze_lead_node)


workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", END)

# کامپایل موتور گراف
agent_app = workflow.compile()


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
