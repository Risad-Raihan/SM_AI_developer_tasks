from fastapi import APIRouter, HTTPException, Depends
from app.api.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from app.services.chat import ChatService
from typing import List

router = APIRouter()
chat_service = ChatService()

@router.post("/chat", 
    response_model=ChatResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Chat with the restaurant assistant",
    description="Send a message to the restaurant chatbot and get a response with suggested actions."
)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = await chat_service.process_message(
            user_id=request.user_id,
            message=request.message,
            session_id=request.session_id
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 