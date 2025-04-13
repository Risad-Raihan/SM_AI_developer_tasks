# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEMO_MODE=True

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install only the required dependencies for the API
RUN pip install fastapi==0.115.12 \
    uvicorn==0.34.0 \
    motor==3.7.0 \
    pydantic==2.11.3 \
    pydantic-settings==2.8.1 \
    python-dotenv==1.1.0 \
    python-multipart==0.0.20 \
    requests==2.32.3 \
    typing-extensions==4.13.2

# Copy application files
COPY app ./app
COPY vectorstore ./vectorstore
COPY .env .
COPY init_db.py .

# Create demo response file
RUN echo '{\
    "menu_inquiry": "Yes, we have several vegetarian options including our Bruschetta Classica, Caprese Salad, and Quattro Formaggi Pizza. Would you like to hear more details about any of these dishes?",\
    "reservation_request": "Id be happy to help you with a reservation. Could you please provide the date, time, and number of guests?",\
    "hours_location": "Savory Haven is located at 789 Gourmet Avenue, Flavor Town, CA 90210. Our hours are Monday-Thursday 11am-10pm, Friday-Saturday 11am-11pm, and Sunday 11am-9pm.",\
    "special_events": "We have a special Wine Wednesday event with half-price bottles of select wines. This Friday we also have a live jazz band performing from 7-9pm.",\
    "default": "Thank you for your question. Our staff would be happy to assist you. Is there anything specific about our menu, hours, or specials that youd like to know about?"\
}' > /app/app/demo_responses.json

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 