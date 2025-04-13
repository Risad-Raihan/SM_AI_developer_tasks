# Savory Haven Restaurant Chatbot

A conversational AI system for "Savory Haven" restaurant using FastAPI, Docker, and NLP. This chatbot helps customers get information about the menu, make reservations, and answer common questions about the restaurant.

## Project Overview

This project implements a restaurant chatbot API with the following features:
- Natural language processing to understand customer queries
- Intent detection for menu inquiries, reservations, hours/location, and special events
- MongoDB integration for data persistence
- Docker containerization for easy deployment
- Deployed on Render cloud platform

## Key Components

- **FastAPI Backend**: Implements the chat and health endpoints
- **NLP Pipeline**: Uses RAG (Retrieval Augmented Generation) for smart responses
- **Vector Store**: FAISS-based semantic search for restaurant information
- **Docker Support**: Complete containerization with Docker and Docker Compose
- **Cloud Deployment**: Deployed and accessible on Render

## Live Demo

The application is deployed and accessible at:
- **API Documentation**: [https://savory-haven-chatbot.onrender.com/docs](https://savory-haven-chatbot.onrender.com/docs)
- **Health Check**: [https://savory-haven-chatbot.onrender.com/health](https://savory-haven-chatbot.onrender.com/health)

## Implementation Details

Due to GitHub file size limitations, the complete project code (including the vector store and dependencies) is available in a zip file hosted on Google Drive:

[Download Full Project (Google Drive Link)](https://drive.google.com/drive/folders/YOUR_FOLDER_ID)

## Project Structure

```
savory-haven-chatbot/
├── app/                      # Main application code
│   ├── api/                  # API endpoints
│   ├── core/                 # Core configuration
│   ├── db/                   # Database models and connection
│   └── services/             # Business logic and NLP services
├── data/                     # Restaurant dataset
├── docs/                     # Documentation and screenshots
├── vectorstore/              # FAISS vector store
├── Dockerfile                # Main Docker configuration
├── Dockerfile.demo           # Simplified Docker for demo
├── docker-compose.yml        # Docker Compose configuration
├── app.py                    # Main application entry point
├── demo_app.py               # Simplified demo application
└── requirements.txt          # Python dependencies
```

## Documentation

Complete API documentation is available in the `docs/` directory, including:
- API endpoints and schema definitions
- Test scenarios and example responses
- Docker deployment instructions
- Render deployment guide

## Technologies Used

- FastAPI
- MongoDB
- Docker and Docker Compose
- FAISS Vector Database
- Sentence Transformers
- Render Cloud Platform
