from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str

class SuggestedAction(BaseModel):
    action_type: str
    label: str
    value: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    intent: str
    suggested_actions: List[SuggestedAction] = []
    timestamp: datetime = datetime.utcnow()

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 