# Converting Documentation to PDF

To convert the API documentation to PDF format, follow these steps:

## Using Pandoc (Recommended)

1. Install Pandoc from https://pandoc.org/installing.html

2. Install a PDF engine like wkhtmltopdf from https://wkhtmltopdf.org/downloads.html

3. Open a terminal and navigate to the docs folder:
   ```
   cd docs
   ```

4. Run the following command:
   ```
   pandoc api_documentation.md -o savory_haven_api_documentation.pdf --pdf-engine=wkhtmltopdf
   ```

## Alternative Method: Using a Markdown Editor

1. Open the `api_documentation.md` file in a Markdown editor that supports PDF export (such as Typora, Visual Studio Code with extensions, or an online converter like https://www.markdowntopdf.com/)

2. Export/Save as PDF

## PDF Content Requirements

The PDF documentation should include:

1. **Title Page**: 
   - Project Name: Savory Haven Restaurant Chatbot
   - Author Name
   - Date
   - Organization/Course Name

2. **Table of Contents**

3. **API Documentation**:
   - All content from the api_documentation.md file
   - Screenshots of the Swagger UI

4. **Appendix**:
   - Test results
   - Sample responses

Make sure all Swagger UI screenshots are properly included in the PDF documentation. 