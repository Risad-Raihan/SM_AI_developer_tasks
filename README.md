# Savory Haven Restaurant Chatbot

A conversational AI system for Savory Haven restaurant built with FastAPI and MongoDB. This chatbot helps customers get information about the menu, make reservations, and answer common questions about the restaurant.

## Features

- **Natural Language Understanding**: Understands and responds to customer queries
- **Intent Recognition**: Identifies user intents like menu inquiries, reservation requests, etc.
- **Retrieval Augmented Generation (RAG)**: Uses vector search to provide accurate information
- **Conversation History**: Maintains context across messages
- **Suggested Actions**: Provides relevant action options based on the conversation

## Core Functionalities

- **Menu Browsing**: Get information about menu items, including prices and dietary options
- **Reservation Handling**: Make reservations and check availability
- **Restaurant Information**: Check hours, location, and other details
- **Special Events**: Learn about promotions, happy hours, and special events

## Technology Stack

- **Backend**: FastAPI
- **Database**: MongoDB
- **Vector Store**: FAISS
- **Language Model**: Google Gemini
- **Embedding Model**: Sentence Transformers

## API Endpoints

### POST /api/chat

Process a user message and return a response.

**Request:**
```json
{
  "user_id": "user123",
  "message": "Do you have any vegetarian options on the menu?",
  "session_id": "session456"
}
```

**Response:**
```json
{
  "response": "Yes, we have several vegetarian options including our Bruschetta Classica, Caprese Salad, and Quattro Formaggi Pizza. Would you like more details about any of these dishes?",
  "intent": "menu_inquiry",
  "suggested_actions": [
    {
      "action_type": "view_menu",
      "label": "View Full Menu",
      "value": "full_menu"
    },
    {
      "action_type": "filter_menu",
      "label": "Filter by Category",
      "value": "categories"
    }
  ],
  "timestamp": "2023-07-15T14:32:10Z"
}
```

### GET /health

Check if the API is running.

## Setup and Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/restaurant-chatbot.git
cd restaurant-chatbot
```

2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables by creating a `.env` file:
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=restaurant_chatbot
GEMINI_API_KEY=your_gemini_api_key
```

5. Initialize the database
```bash
python init_db.py
```

6. Create the vector store
```bash
python create_vector_store.py
```

7. Start the server
```bash
uvicorn app.main:app --reload
```

## Docker Deployment

1. Build the Docker image
```bash
docker-compose build
```

2. Run the container
```bash
docker-compose up
```

## Project Structure

```
restaurant-chatbot/
├── app/
│   ├── api/
│   │   ├── models/
│   │   │   └── schemas.py
│   │   └── routes/
│   │       └── chat.py
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── models.py
│   │   └── mongodb.py
│   ├── services/
│   │   ├── chat.py
│   │   ├── intent.py
│   │   ├── llm.py
│   │   └── rag.py
│   └── main.py
├── data/
│   └── res-bot-dataset.json
├── vectorstore/
│   └── db_faiss/
├── .env
├── create_vector_store.py
├── docker-compose.yml
├── Dockerfile
├── init_db.py
├── requirements.txt
└── test_api.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 