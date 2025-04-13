from typing import List, Optional
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from app.core.config import settings
from app.services.llm import GeminiLLM

class RAGService:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.vector_store = FAISS.load_local(
            settings.VECTOR_STORE_PATH,
            self.embedding_model,
            allow_dangerous_deserialization=True
        )
        self.llm = GeminiLLM(
            gemini_api_key=settings.GEMINI_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
        self._setup_prompts()

    def _setup_prompts(self):
        # Base prompt template
        self.base_prompt = PromptTemplate(
            template="""You are a helpful restaurant assistant for {restaurant_name}. 
            Use the following context to answer the question. If you don't know the answer, 
            just say that you don't know, don't try to make up an answer.

            Context: {context}

            Question: {question}

            Answer: """,
            input_variables=["context", "question", "restaurant_name"]
        )

        # Intent-specific prompts
        self.intent_prompts = {
            "menu_inquiry": PromptTemplate(
                template="""You are a helpful restaurant assistant for {restaurant_name}. 
                The user is asking about the menu. Use the following context about our menu items 
                to provide a detailed and appetizing response. Include prices and highlight any 
                special features or dietary accommodations.

                Context: {context}

                Question: {question}

                Answer: """,
                input_variables=["context", "question", "restaurant_name"]
            ),
            "reservation_request": PromptTemplate(
                template="""You are a helpful restaurant assistant for {restaurant_name}. 
                The user wants to make a reservation. Use the following context about our 
                reservation policies and availability to help them. Be sure to ask for any 
                missing information needed for the reservation.

                Context: {context}

                Question: {question}

                Answer: """,
                input_variables=["context", "question", "restaurant_name"]
            ),
            "hours_location": PromptTemplate(
                template="""You are a helpful restaurant assistant for {restaurant_name}. 
                The user is asking about our hours or location. Use the following context 
                to provide clear and accurate information about when we're open and where 
                to find us.

                Context: {context}

                Question: {question}

                Answer: """,
                input_variables=["context", "question", "restaurant_name"]
            )
        }

    async def get_response(self, query: str, intent: str) -> str:
        # Get relevant documents from vector store
        docs = self.vector_store.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # Select appropriate prompt based on intent
        prompt = self.intent_prompts.get(intent, self.base_prompt)
        
        # Define input variables including restaurant_name
        input_variables = {
            "query": query,
            "context": context,
            "question": query,
            "restaurant_name": settings.RESTAURANT_NAME
        }
        
        # Use prompt directly instead of creating a chain
        formatted_prompt = prompt.format(**input_variables)
        
        # Send to LLM
        result = await self.llm.agenerate([formatted_prompt])
        return result.generations[0][0].text 