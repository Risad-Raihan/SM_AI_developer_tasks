# Deployment Guide for Savory Haven Restaurant Chatbot

This guide provides step-by-step instructions for deploying the Savory Haven Restaurant Chatbot using Docker and Render.

## Docker Deployment

### Prerequisites
- Docker Desktop installed on your machine
- Docker Compose installed
- Git repository cloned locally

### Local Deployment Steps

1. Make sure your `.env` file is set up with the following variables:
   ```
   MONGODB_URL=mongodb://mongodb:27017
   MONGODB_DB_NAME=restaurant_chatbot
   GEMINI_API_KEY=your_gemini_api_key
   ```

2. Build the Docker containers:
   ```bash
   docker-compose build
   ```

3. Run the application:
   ```bash
   docker-compose up
   ```

4. Access the application at `http://localhost:8000/docs`

5. To stop the application:
   ```bash
   docker-compose down
   ```

### Docker Image Management

1. Tag the Docker image:
   ```bash
   docker tag restaurant-chatbot:latest yourusername/restaurant-chatbot:latest
   ```

2. Push to Docker Hub (optional):
   ```bash
   docker login
   docker push yourusername/restaurant-chatbot:latest
   ```

## Deployment to Render

Render is a unified cloud platform that makes it easy to deploy applications. Here's how to deploy the restaurant chatbot to Render:

### Prerequisites
- A Render account (https://render.com)
- A GitHub repository with your project code

### Deployment Steps

1. **Create a MongoDB Database**:
   - Log in to Render dashboard
   - Click "New" → "Database"
   - Select "MongoDB"
   - Name it "restaurant-chatbot-db"
   - Choose a region close to your users
   - Select a plan (Free tier is available)
   - Click "Create Database"
   - Note the connection details provided (you'll need these for the next step)

2. **Deploy the Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Name: "restaurant-chatbot"
   - Region: Choose the same region as your database
   - Environment: "Docker"
   - Branch: "main" (or your preferred branch)
   - Set the following environment variables:
     - `MONGODB_URL`: Use the connection string from your Render MongoDB instance
     - `MONGODB_DB_NAME`: restaurant_chatbot
     - `GEMINI_API_KEY`: Your Google Gemini API key
   - Select a plan (Starter plan recommended)
   - Click "Create Web Service"

3. **Initialize the Database**:
   - After deployment, go to the "Shell" tab of your web service
   - Run the following commands:
     ```bash
     python init_db.py
     python create_vector_store.py
     ```

4. **Verify Deployment**:
   - Click on the URL of your deployed application
   - Navigate to `/docs` to view the Swagger UI documentation
   - Test the API endpoints

### Updating the Deployed Application

When you push changes to your GitHub repository, Render will automatically rebuild and deploy your application.

## Troubleshooting

### Common Docker Issues

1. **Port Conflicts**:
   - If port 8000 is already in use, change the port mapping in your `docker-compose.yml`
   - Example: `"8001:8000"` (this maps local port 8001 to container port 8000)

2. **MongoDB Connection Issues**:
   - Ensure MongoDB container is running: `docker ps`
   - Check MongoDB logs: `docker logs <container_id>`

3. **Volume Permissions**:
   - If you encounter permission issues with volumes, run:
     ```bash
     chmod -R 777 ./vectorstore
     ```

### Common Render Issues

1. **Failed Builds**:
   - Check build logs for errors
   - Ensure your Dockerfile is valid
   - Verify all required files are committed to your repository

2. **Environment Variables**:
   - Double-check that all required environment variables are set correctly
   - Make sure there are no typos in environment variable names

3. **MongoDB Connection**:
   - Ensure the MongoDB connection string is correct
   - Check network rules to ensure the web service can access the database

## Monitoring and Maintenance

1. **Monitoring**:
   - Use Render's built-in monitoring tools
   - Check application logs regularly

2. **Scaling**:
   - Render allows you to scale your application by changing the plan
   - Consider upgrading if you experience high traffic

3. **Backups**:
   - Regularly backup your MongoDB database
   - Render provides automatic backups for paid database plans 