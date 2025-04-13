"""
Entry point for Render deployment
"""
from demo_app import app

# This file allows Render to import the app directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 