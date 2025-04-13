import json
import os
from typing import Dict, List, Any
import random
from datetime import datetime
from pydantic import BaseModel
from app.core.config import settings
from app.db.mongodb import conversations
from app.api.models.schemas import ChatResponse, SuggestedAction
from app.services.intent import IntentService

# Only import RAG when not in demo mode
if not os.environ.get("DEMO_MODE"):
    from app.services.rag import RAGService
    rag_service = RAGService()

# Demo responses
DEMO_RESPONSES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "demo_responses.json")

class SuggestedAction(BaseModel):
    action_type: str
    label: str
    value: str

class ChatService:
    def __init__(self):
        self.demo_mode = os.environ.get("DEMO_MODE", "False").lower() in ["true", "1", "t"]
        if self.demo_mode and os.path.exists(DEMO_RESPONSES_PATH):
            with open(DEMO_RESPONSES_PATH, "r") as f:
                self.demo_responses = json.load(f)
        else:
            self.demo_responses = {
                "default": "Thank you for your question. Our staff would be happy to assist you."
            }
        self.intent_service = IntentService()

    async def process_message(self, user_id: str, message: str, session_id: str) -> Dict[str, Any]:
        """Process user message and generate a response"""
        
        # Generate timestamp
        timestamp = datetime.now().isoformat()
        
        if self.demo_mode:
            # Demo mode: use pre-defined responses
            return self._get_demo_response(message, timestamp)
        else:
            # Normal mode: use RAG
            try:
                # Get response from RAG
                rag_result = rag_service.get_response(message)
                response_text = rag_result["answer"]
                intent = self._detect_intent(message, rag_result.get("sources", []))
                
                # Generate suggested actions based on intent
                suggested_actions = self._generate_suggested_actions(intent)
                
                return {
                    "response": response_text,
                    "intent": intent,
                    "suggested_actions": suggested_actions,
                    "timestamp": timestamp
                }
            except Exception as e:
                print(f"Error in RAG service: {e}")
                return {
                    "response": "I'm sorry, I encountered an error processing your request.",
                    "intent": "error",
                    "suggested_actions": [],
                    "timestamp": timestamp
                }
    
    def _get_demo_response(self, message: str, timestamp: str) -> Dict[str, Any]:
        """Get a demo response based on simple keyword matching"""
        message = message.lower()
        
        intent = "default"
        if any(word in message for word in ["vegetarian", "vegan", "gluten", "menu", "food", "dish", "eat"]):
            intent = "menu_inquiry"
        elif any(word in message for word in ["reservation", "book", "table", "reserve", "booking"]):
            intent = "reservation_request"
        elif any(word in message for word in ["hour", "open", "close", "location", "address", "where", "when"]):
            intent = "hours_location"
        elif any(word in message for word in ["event", "special", "promotion", "offer", "deal", "discount"]):
            intent = "special_events"
        
        response = self.demo_responses.get(intent, self.demo_responses["default"])
        suggested_actions = self._generate_suggested_actions(intent)
        
        return {
            "response": response,
            "intent": intent,
            "suggested_actions": suggested_actions,
            "timestamp": timestamp
        }
    
    def _detect_intent(self, message: str, sources: List[Dict[str, Any]]) -> str:
        """Detect intent based on user message and retrieved sources"""
        message = message.lower()
        
        # Simple rule-based intent detection
        if any(word in message for word in ["vegetarian", "vegan", "gluten", "menu", "food", "dish", "eat"]):
            return "menu_inquiry"
        elif any(word in message for word in ["reservation", "book", "table", "reserve", "booking"]):
            return "reservation_request"
        elif any(word in message for word in ["hour", "open", "close", "location", "address", "where", "when"]):
            return "hours_location"
        elif any(word in message for word in ["event", "special", "promotion", "offer", "deal", "discount"]):
            return "special_events"
        else:
            return "general_inquiry"
    
    def _generate_suggested_actions(self, intent: str) -> List[Dict[str, str]]:
        """Generate suggested actions based on intent"""
        if intent == "menu_inquiry":
            return [
                SuggestedAction(
                    action_type="view_menu",
                    label="View Full Menu",
                    value="full_menu"
                ),
                SuggestedAction(
                    action_type="filter_menu",
                    label="Filter by Category",
                    value="categories"
                )
            ]
        elif intent == "reservation_request":
            return [
                SuggestedAction(
                    action_type="make_reservation",
                    label="Make Reservation",
                    value="reservation_form"
                )
            ]
        elif intent == "hours_location":
            return [
                SuggestedAction(
                    action_type="view_hours",
                    label="View Opening Hours",
                    value="hours"
                )
            ]
        else:
            return []

    async def _store_conversation(
        self,
        user_id: str,
        session_id: str,
        message: str,
        response: ChatResponse
    ):
        conversation = {
            "user_id": user_id,
            "session_id": session_id,
            "messages": [
                {
                    "role": "user",
                    "content": message,
                    "timestamp": datetime.utcnow()
                },
                {
                    "role": "assistant",
                    "content": response.response,
                    "timestamp": response.timestamp
                }
            ],
            "intent": response.intent,
            "suggested_actions": [action.model_dump() for action in response.suggested_actions],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        await conversations.insert_one(conversation) 