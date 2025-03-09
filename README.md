# MediBot: AI-Powered Medical Assistant with RAG Technology

![MediBot Logo](https://img.icons8.com/color/96/000000/robot.png)

## Overview

MediBot is an AI-powered medical assistant that uses Retrieval-Augmented Generation (RAG) technology to provide accurate medical information from trusted references. The system integrates knowledge from multiple medical textbooks and provides source-based responses with proper citations.

## Features

- **Multi-source Knowledge Base**: Integrates information from:
  - The Gale Encyclopedia of Medicine (Second Edition)
  - Davidson's Principles and Practice of Medicine (24th Edition)

- **Intelligent RAG Pipeline**:
  - Semantic search using vector embeddings
  - Context-aware responses with source citations
  - Page number references for verification

- **Advanced Visualization**:
  - Automatic table detection and extraction
  - Interactive data visualization
  - Charts for time-series and comparison data

- **User Experience**:
  - Intuitive chat interface
  - Conversation history tracking
  - Response feedback mechanism
  - Chat history download functionality
  - Clear chat option

## Technical Architecture

### Components

1. **Data Processing**:
   - PDF text extraction with PyPDF2
   - Document chunking with RecursiveCharacterTextSplitter
   - Metadata preservation (source, page number)

2. **Vector Database**:
   - Embeddings generation with sentence-transformers
   - FAISS vector store for similarity search
   - Updatable knowledge base

3. **LLM Integration**:
   - Google Gemini 2.0 Flash API for response generation
   - Custom prompt templates
   - RetrievalQA chain implementation

4. **Web Interface**:
   - Streamlit-based chat UI
   - Responsive design
   - Informative sidebar

## Installation

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Risad-Raihan/Medibot.git
   cd Medibot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows
   .\.venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     ```

5. Prepare your data:
   - Place PDF files in the `data/` directory

6. Create the vector store:
   ```bash
   python create_memory_for_llm.py
   ```

7. Run the application:
   ```bash
   python run_medibot.py
   ```

## Usage

1. Access the web interface at `http://localhost:8501`
2. Type your medical question in the chat input
3. View the response with source citations
4. Use the feedback buttons to rate responses
5. Download your chat history if needed

## Project Structure

```
medical-chatbot/
├── data/                      # PDF files directory
├── vectorstore/               # FAISS vector store
├── create_memory_for_llm.py   # Vector store creation script
├── update_vector_store.py     # Script to add new references
├── connect_memory_with_llm.py # LLM connection script
├── medibot.py                 # Main Streamlit application
├── run_medibot.py             # Script to run with warnings suppressed
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Technologies Used

- **Python**: Core programming language
- **LangChain**: Framework for building LLM applications
- **Streamlit**: Web application framework
- **FAISS**: Vector database for similarity search
- **Google Gemini API**: For generating responses
- **HuggingFace**: For embeddings
- **PyPDF2**: For PDF text extraction
- **Pandas & Matplotlib**: For data visualization

## Future Enhancements

- Integration with medical imaging analysis
- Support for more medical references
- Enhanced visualization capabilities
- Mobile application version

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Gale Encyclopedia of Medicine
- Davidson's Principles and Practice of Medicine
- Google for providing access to the Gemini API
- The LangChain community for the excellent RAG framework

---

Created by [Risad Raihan](https://github.com/Risad-Raihan) 