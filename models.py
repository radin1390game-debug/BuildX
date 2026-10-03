from pydantic import BaseModel, Field

class LeadAnalysis(BaseModel):
    is_potential_lead: bool = Field(description="Whether the user is a potential lead")
    relevance_score: int = Field(description="Score between 0 and 100")
    reasoning: str = Field(description="Reasoning behind the evaluation")
    suggested_reply: str = Field(description="Suggested Persian reply to send")