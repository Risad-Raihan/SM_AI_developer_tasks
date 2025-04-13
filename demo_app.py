import json
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import random

# Create a simple FastAPI application for the demo
app = FastAPI(
    title="Savory Haven Restaurant Chatbot",
    description="A conversational AI system for Savory Haven restaurant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample demo responses
DEMO_RESPONSES = {
    "menu_inquiry": "Yes, we have several vegetarian options including our Bruschetta Classica, Caprese Salad, and Quattro Formaggi Pizza. Would you like to hear more details about any of these dishes?",
    "reservation_request": "I'd be happy to help you with a reservation. Could you please provide the date, time, and number of guests?",
    "hours_location": "Savory Haven is located at 789 Gourmet Avenue, Flavor Town, CA 90210. Our hours are Monday-Thursday 11am-10pm, Friday-Saturday 11am-11pm, and Sunday 11am-9pm.",
    "special_events": "We have a special Wine Wednesday event with half-price bottles of select wines. This Friday we also have a live jazz band performing from 7-9pm.",
    "default": "Thank you for your question. Our staff would be happy to assist you. Is there anything specific about our menu, hours, or specials that you'd like to know about?"
}

# Models
class ChatRequest(BaseModel):
    user_id: str
    message: str
    session_id: str

class SuggestedAction(BaseModel):
    action_type: str
    label: str
    value: str

class ChatResponse(BaseModel):
    response: str
    intent: str
    suggested_actions: List[SuggestedAction] = []
    timestamp: str = None

# Helper functions
def detect_intent(message: str) -> str:
    """Simple intent detection based on keywords"""
    message = message.lower()
    
    if any(word in message for word in ["vegetarian", "vegan", "gluten", "menu", "food", "dish", "eat"]):
        return "menu_inquiry"
    elif any(word in message for word in ["reservation", "book", "table", "reserve", "booking"]):
        return "reservation_request"
    elif any(word in message for word in ["hour", "open", "close", "location", "address", "where", "when"]):
        return "hours_location"
    elif any(word in message for word in ["event", "special", "promotion", "offer", "deal", "discount"]):
        return "special_events"
    else:
        return "default"

def generate_suggested_actions(intent: str) -> List[SuggestedAction]:
    """Generate suggested actions based on intent"""
    if intent == "menu_inquiry":
        return [
            SuggestedAction(action_type="view_menu", label="View Full Menu", value="full_menu"),
            SuggestedAction(action_type="filter_menu", label="Filter by Category", value="categories")
        ]
    elif intent == "reservation_request":
        return [
            SuggestedAction(action_type="make_reservation", label="Make Reservation", value="reservation_form")
        ]
    elif intent == "hours_location":
        return [
            SuggestedAction(action_type="view_hours", label="View Opening Hours", value="hours")
        ]
    else:
        return []

# Endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat messages"""
    message = request.message
    
    # Detect intent
    intent = detect_intent(message)
    
    # Get response
    response = DEMO_RESPONSES.get(intent, DEMO_RESPONSES["default"])
    
    # Generate suggested actions
    suggested_actions = generate_suggested_actions(intent)
    
    # Create timestamp
    timestamp = datetime.now().isoformat()
    
    return ChatResponse(
        response=response,
        intent=intent,
        suggested_actions=suggested_actions,
        timestamp=timestamp
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Savory Haven Restaurant Chatbot (Demo)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 