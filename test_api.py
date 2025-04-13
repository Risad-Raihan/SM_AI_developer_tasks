import httpx
import asyncio
import json
from datetime import datetime

async def test_chat_endpoint():
    async with httpx.AsyncClient() as client:
        # Test menu inquiry
        menu_request = {
            "user_id": "test_user_1",
            "message": "What vegetarian options do you have on the menu?",
            "session_id": "test_session_1"
        }
        response = await client.post(
            "http://localhost:8000/api/chat",
            json=menu_request
        )
        print("\nMenu Inquiry Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test reservation request
        reservation_request = {
            "user_id": "test_user_2",
            "message": "I'd like to make a reservation for 4 people tomorrow at 7 PM",
            "session_id": "test_session_2"
        }
        response = await client.post(
            "http://localhost:8000/api/chat",
            json=reservation_request
        )
        print("\nReservation Request Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test hours and location
        hours_request = {
            "user_id": "test_user_3",
            "message": "What are your opening hours and where are you located?",
            "session_id": "test_session_3"
        }
        response = await client.post(
            "http://localhost:8000/api/chat",
            json=hours_request
        )
        print("\nHours and Location Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        # Test special events
        events_request = {
            "user_id": "test_user_4",
            "message": "Are there any special events or promotions happening this week?",
            "session_id": "test_session_4"
        }
        response = await client.post(
            "http://localhost:8000/api/chat",
            json=events_request
        )
        print("\nSpecial Events Test:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_chat_endpoint()) 