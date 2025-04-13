# Instructions for Taking Documentation Screenshots

To complete the API documentation, you need to take several screenshots of the Swagger UI interface. Follow these steps to capture the required screenshots:

## Step 1: Start the Server

1. Open a terminal
2. Navigate to your project directory
3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Step 2: Access the Swagger UI

1. Open your web browser
2. Navigate to `http://localhost:8000/docs`
3. Wait for the Swagger UI to load completely

## Step 3: Take Required Screenshots

### 1. Swagger UI Overview (swagger_overview.png)

Take a screenshot of the entire Swagger UI page showing all available endpoints (without expanding any of them). This should show:
- The API title
- The health endpoint
- The chat endpoint
- The schemas section (collapsed)

### 2. Chat Endpoint Documentation (swagger_chat_endpoint.png)

1. Click on the POST `/api/chat` endpoint to expand it
2. Ensure the Request Body section is visible
3. Take a screenshot that shows:
   - The endpoint description
   - The request body schema
   - The response schemas

### 3. Health Endpoint Documentation (swagger_health_endpoint.png)

1. Click on the GET `/health` endpoint to expand it
2. Take a screenshot that shows:
   - The endpoint description
   - The response schema

### 4. Schema Documentation (swagger_schemas.png)

1. Scroll down to the Schemas section
2. Expand all relevant schemas (ChatRequest, ChatResponse, SuggestedAction, ErrorResponse)
3. Take a screenshot showing all expanded schemas

## Step 4: Save the Screenshots

1. Save all screenshots to the `docs` folder in your project
2. Use the exact filenames mentioned above:
   - `swagger_overview.png`
   - `swagger_chat_endpoint.png`
   - `swagger_health_endpoint.png`
   - `swagger_schemas.png`

## Step 5: Include Screenshots in Documentation

These screenshots should be included in:
1. The Markdown documentation (`api_documentation.md`)
2. The PDF version of the documentation
3. Any project submission documents

## Tips for Good Screenshots

1. Use a clean browser window without excessive toolbars or extensions
2. Make sure the Swagger UI is properly expanded to show all relevant information
3. Ensure the text is readable (not too small)
4. Use a screen capture tool that allows for clean, cropped screenshots
5. Consider using tools like Snipping Tool (Windows), Screenshot (Mac), or browser extensions 