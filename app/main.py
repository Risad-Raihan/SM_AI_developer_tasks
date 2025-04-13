from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.db.mongodb import MongoDB

app = FastAPI(
    title="Savory Haven Restaurant Chatbot",
    description="A conversational AI system for Savory Haven restaurant",
    version="1.0.0",
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers for database connection
@app.on_event("startup")
async def startup_db_client():
    await MongoDB.connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await MongoDB.close_mongo_connection()

# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Savory Haven Restaurant Chatbot API",
        version="1.0.0",
        description="API for Savory Haven restaurant chatbot",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Savory Haven Restaurant Chatbot API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Savory Haven Restaurant Chatbot"}

# Import and include routers
from app.api.routes import chat
app.include_router(chat.router, prefix="/api", tags=["chat"]) 