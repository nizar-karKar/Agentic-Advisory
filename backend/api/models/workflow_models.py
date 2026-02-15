from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class WorkflowRequest(BaseModel):
    question: str = Field(..., min_length=5)
    max_iterations: int = Field(default=2, ge=1, le=5)


class WorkflowResponse(BaseModel):
    final_answer: str
    iterations: int
    critique: Optional[Dict[str, Any]] = None
