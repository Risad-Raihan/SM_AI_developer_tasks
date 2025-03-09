import os
import streamlit as st
import re
from datetime import datetime
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import requests
import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.llms.base import LLM
from typing import Any, List, Mapping, Optional

## Uncomment the following files if you're not using pipenv as your virtual environment manager
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Define Gemini LLM class
class GeminiLLM(LLM):
    gemini_api_key: str
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.5
    max_tokens: int = 512
    
    @property
    def _llm_type(self) -> str:
        return "gemini"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.gemini_api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        if self.temperature is not None:
            data["generationConfig"] = {"temperature": self.temperature}
        
        if self.max_tokens is not None:
            if "generationConfig" not in data:
                data["generationConfig"] = {}
            data["generationConfig"]["maxOutputTokens"] = self.max_tokens
        
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code != 200:
            raise ValueError(f"Error from Gemini API: {response.text}")
        
        response_json = response.json()
        
        # Extract the generated text from the response
        try:
            generated_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            return generated_text
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected response format from Gemini API: {str(e)}")
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }


DB_FAISS_PATH="vectorstore/db_faiss"
@st.cache_resource
def get_vectorstore():
    embedding_model=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    db=FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db


def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt


def load_llm():
    # Get the Gemini API key from environment variables
    gemini_api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyA3Pd3lpzpvFmSaczIIvPzOU-6m1tujg7Q")
    
    # Create and return the Gemini LLM
    llm = GeminiLLM(
        gemini_api_key=gemini_api_key,
        temperature=0.5,
        max_tokens=512
    )
    return llm


def is_greeting_or_general_query(text):
    """Check if the input is a greeting or general query that doesn't need RAG."""
    text = text.lower().strip()
    
    # Define patterns for greetings and general queries
    greeting_patterns = [
        r'^hi$', r'^hello$', r'^hey$', r'^hi there$', r'^hello there$',
        r'^greetings$', r'^howdy$', r'^good morning$', r'^good afternoon$',
        r'^good evening$', r'^what\'s up$', r'^how are you$', r'^how are you doing$',
        r'^how do you work$', r'^what can you do$', r'^who are you$',
        r'^what are you$', r'^tell me about yourself$', r'^introduce yourself$'
    ]
    
    # Check if the input matches any greeting pattern
    for pattern in greeting_patterns:
        if re.match(pattern, text):
            return True
    
    return False


def get_general_response(query):
    """Generate responses for greetings and general queries."""
    query = query.lower().strip()
    
    if re.match(r'^(hi|hello|hey|greetings|howdy)( there)?$', query):
        return "Hello Dr. Moumi! I'm MediBot, your medical information assistant. I can answer questions about medical conditions, treatments, and health topics based on The Gale Encyclopedia of Medicine and Davidson's Medicine. How can I help you today?"
    
    elif re.match(r'^(good morning|good afternoon|good evening)$', query):
        return "Good day Dr. Moumi! I'm MediBot, your medical information assistant. I can provide information about various medical topics from multiple medical references. What would you like to know?"
    
    elif re.match(r'^(how are you|how are you doing|what\'s up)$', query):
        return "I'm functioning well, thank you for asking Dr. Moumi! I'm here to provide you with medical information from trusted medical references. What medical topic would you like to learn about?"
    
    elif re.match(r'^(who are you|what are you|tell me about yourself|introduce yourself)$', query):
        return "I'm MediBot, an AI assistant specialized in medical information created for Dr. Moumi. I was built using multiple medical references including The Gale Encyclopedia of Medicine and Davidson's Medicine 24th Edition. I can provide information on various medical conditions, treatments, procedures, and health topics. My knowledge is based on the content of these medical references, so I can help answer specific medical questions you might have."
    
    elif re.match(r'^(how do you work|what can you do)$', query):
        return "I work by searching through multiple medical references to find relevant information about your medical questions, Dr. Moumi. When you ask me a specific medical question, I search for the most relevant information in my knowledge base and provide you with accurate answers based on The Gale Encyclopedia of Medicine and Davidson's Medicine. I can help with questions about diseases, treatments, symptoms, medical procedures, and general health topics."
    
    else:
        return None  # Not a general query, use RAG


def extract_tabular_data(text):
    """
    Attempt to extract tabular data from text.
    Returns a tuple of (is_table, table_data, table_title)
    """
    # Common patterns that indicate tabular data
    table_indicators = [
        r'Table \d+[\.:]',
        r'Figure \d+[\.:]',
        r'\|\s*[-]+\s*\|',  # Markdown table separator
    ]
    
    # Check if any table indicators are present
    has_table_indicator = any(re.search(pattern, text, re.IGNORECASE) for pattern in table_indicators)
    
    # If no clear table indicators, return early
    if not has_table_indicator:
        return False, None, None
    
    # Try to extract the table title
    title_match = re.search(r'(Table|Figure)\s+\d+[\.:]?\s*([^\n]+)', text, re.IGNORECASE)
    table_title = title_match.group(2).strip() if title_match else "Extracted Table"
    
    # Look for patterns that suggest tabular data
    rows = text.split('\n')
    
    # Try to parse the table data
    try:
        # For markdown-style tables with pipe separators
        if '|' in text and any('|' in row and '-' in row for row in rows):
            # Find rows with pipe separators
            table_rows = [row.strip() for row in rows if '|' in row]
            
            # Need at least 3 rows for a valid table (header, separator, data)
            if len(table_rows) < 3:
                return False, None, None
                
            # Check for separator row (like |---|---|)
            has_separator = any(re.match(r'^[\|\s\-:]+$', row) for row in table_rows)
            if not has_separator:
                return False, None, None
            
            # Extract headers (first row)
            header_row = table_rows[0]
            headers = [h.strip() for h in header_row.split('|') if h.strip()]
            
            # Find separator row index
            separator_idx = next((i for i, row in enumerate(table_rows) if re.match(r'^[\|\s\-:]+$', row)), 1)
            
            # Extract data rows (after separator)
            data = []
            for row in table_rows[separator_idx+1:]:
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                if cells and len(cells) == len(headers):  # Ensure row has same number of columns as header
                    data.append(cells)
            
            # If we have headers and data, create DataFrame
            if headers and data:
                df = pd.DataFrame(data, columns=headers)
                
                # Try to convert numeric columns
                for col in df.columns:
                    try:
                        df[col] = pd.to_numeric(df[col])
                    except:
                        pass
                
                return True, df, table_title
        
        # For tables with clear column headers and consistent structure
        elif title_match:
            # Find potential table rows after the title
            title_idx = next((i for i, row in enumerate(rows) if title_match.group(0) in row), 0)
            potential_table_rows = rows[title_idx+1:title_idx+15]  # Look at next 15 lines max
            
            # Check for consistent column structure
            col_counts = [len(row.split()) for row in potential_table_rows if row.strip()]
            if len(col_counts) >= 3 and col_counts.count(col_counts[0]) >= 3 and col_counts[0] >= 3:
                # First row is likely header
                header_row = potential_table_rows[0].split()
                
                # Extract data rows
                data = []
                for row in potential_table_rows[1:]:
                    cells = row.split()
                    if cells and len(cells) == len(header_row):
                        data.append(cells)
                
                # Create DataFrame
                if data:
                    df = pd.DataFrame(data, columns=header_row)
                    
                    # Try to convert numeric columns
                    for col in df.columns:
                        try:
                            df[col] = pd.to_numeric(df[col])
                        except:
                            pass
                    
                    return True, df, table_title
    
    except Exception as e:
        st.error(f"Error extracting table: {str(e)}")
        return False, None, None
    
    return False, None, None


def display_table_or_chart(df, title):
    """
    Display a DataFrame as a table or chart based on its content.
    """
    st.markdown(f"**{title}**")
    
    # Check if DataFrame is valid
    if df is None or df.empty or df.shape[1] < 2:
        st.warning("Unable to display table: invalid data")
        return
    
    # Check if the DataFrame has numeric columns that could be plotted
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # If we have at least one numeric column and the table isn't too large
    if len(numeric_cols) >= 1 and len(df) <= 20 and len(df.columns) <= 10:
        # Try to determine if this should be a bar chart, line chart, or table
        
        # Check for time series indicators in column names
        time_indicators = ['year', 'month', 'day', 'date', 'time', 'period', 'age']
        has_time_col = any(indicator in col.lower() for col in df.columns.astype(str) for indicator in time_indicators)
        
        # Check for comparison indicators in column names
        comparison_indicators = ['vs', 'comparison', 'compared', 'group', 'category', 'type']
        has_comparison_col = any(indicator in col.lower() for col in df.columns.astype(str) for indicator in comparison_indicators)
        
        # If it looks like time series data, use a line chart
        if has_time_col and len(numeric_cols) >= 1:
            st.line_chart(df[numeric_cols])
            st.dataframe(df)  # Also show the raw data
        
        # If it looks like comparison data, use a bar chart
        elif has_comparison_col or (len(df) <= 10 and len(numeric_cols) >= 1):
            st.bar_chart(df[numeric_cols])
            st.dataframe(df)  # Also show the raw data
        
        # Otherwise, just show as a table
        else:
            st.dataframe(df)
    else:
        # Default to table display
        st.dataframe(df)


def format_source_documents(source_docs):
    """Format source documents to be more readable with proper citations."""
    formatted_sources = []
    table_data = []
    
    for i, doc in enumerate(source_docs, 1):
        # Extract metadata
        metadata = doc.metadata
        source = metadata.get('source', 'Unknown source')
        page = metadata.get('page', 'Unknown page')
        
        # Determine which reference it is
        if "GALE" in source:
            citation = "The Gale Encyclopedia of Medicine, Second Edition"
        elif "Davidson" in source:
            citation = "Davidson's Principles and Practice of Medicine, 24th Edition"
        else:
            citation = source
        
        # Format the source document
        formatted_source = f"**Source {i}:** {os.path.basename(source)}"
        if page != 'Unknown page':
            formatted_source += f" (Page {page})"
        
        # Add citation
        formatted_source += f"\n*Citation: {citation}*"
        
        # Check for tabular data
        is_table, df, table_title = extract_tabular_data(doc.page_content)
        if is_table and df is not None:
            table_data.append((df, f"{table_title} (from {os.path.basename(source)}, Page {page})"))
            # Add a note that a table was extracted
            formatted_source += f"\n> [Table extracted: {table_title}]"
        else:
            # Add a short preview of the content (first 150 chars)
            content_preview = doc.page_content[:150] + "..." if len(doc.page_content) > 150 else doc.page_content
            formatted_source += f"\n> {content_preview}"
        
        formatted_sources.append(formatted_source)
    
    return "\n\n".join(formatted_sources), table_data


def get_download_link(text, filename, link_text):
    """Generate a download link for text content."""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'
    return href


def main():
    # Sidebar with information about the chatbot
    with st.sidebar:
        st.title("MediBot Info")
        st.image("https://img.icons8.com/color/96/000000/robot.png", width=100)
        st.markdown("### About MediBot")
        st.write("MediBot is an AI assistant specialized in medical information, powered by multiple medical references and created for Dr. Moumi.")
        
        st.markdown("### Features")
        st.write("- Answer medical questions using multiple sources")
        st.write("- Provide information on diseases, treatments, and symptoms")
        st.write("- Reference source documents with page numbers")
        st.write("- Compare information across different medical references")
        
        st.markdown("### Data Sources")
        st.write("- The Gale Encyclopedia of Medicine (Second Edition)")
        st.write("- Davidson's Medicine (24th Edition)")
        
        # Add the current date and time
        st.markdown("---")
        st.write(f"Current session: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Search history section
        if 'search_history' in st.session_state and st.session_state.search_history:
            st.markdown("### Recent Searches")
            for idx, query in enumerate(st.session_state.search_history[-5:], 1):
                if not is_greeting_or_general_query(query):
                    st.write(f"{idx}. {query}")
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            if 'search_history' in st.session_state:
                st.session_state.search_history = []
            st.rerun()
            
        # Download chat history
        if 'messages' in st.session_state and len(st.session_state.messages) > 0:
            chat_text = ""
            for msg in st.session_state.messages:
                role = "You" if msg['role'] == 'user' else "MediBot"
                chat_text += f"{role}: {msg['content']}\n\n"
            
            download_filename = f"medibot_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            st.markdown(
                get_download_link(chat_text, download_filename, "Download Chat History"),
                unsafe_allow_html=True
            )

    # Main chat interface
    st.title("Hello Dr. Moumi! Ask MediBot")

    if 'messages' not in st.session_state:
        st.session_state.messages = []
        
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt=st.chat_input("Dr. Moumi, ask me about medical conditions, treatments, or health topics...")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role':'user', 'content': prompt})
        
        # Add to search history if it's not a greeting
        if not is_greeting_or_general_query(prompt):
            st.session_state.search_history.append(prompt)

        # Check if it's a greeting or general query
        general_response = get_general_response(prompt) if is_greeting_or_general_query(prompt) else None
        
        if general_response:
            # If it's a general query, use the predefined response
            st.chat_message('assistant').markdown(general_response)
            st.session_state.messages.append({'role':'assistant', 'content': general_response})
        else:
            # Otherwise, use RAG to answer the medical question
            CUSTOM_PROMPT_TEMPLATE = """
                    Use the pieces of information provided in the context to answer user's question.
                    If you dont know the answer, just say that you dont know, dont try to make up an answer. 
                    Dont provide anything out of the given context

                    Context: {context}
                    Question: {question}

                    Start the answer directly. No small talk please.
                    """
            
            try: 
                # Show a spinner while loading the vector store
                with st.spinner("Searching medical knowledge..."):
                    vectorstore=get_vectorstore()
                    if vectorstore is None:
                        st.error("Failed to load the vector store")
                
                # Show a spinner while generating the response
                with st.spinner("Generating response with Google Gemini..."):
                    qa_chain=RetrievalQA.from_chain_type(
                        llm=load_llm(),
                        chain_type="stuff",
                        retriever=vectorstore.as_retriever(search_kwargs={'k':3}),
                        return_source_documents=True,
                        chain_type_kwargs={'prompt':set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
                    )

                    response=qa_chain.invoke({'query':prompt})

                    result=response["result"]
                    source_documents=response["source_documents"]
                    
                    # Format the source documents
                    formatted_sources, table_data = format_source_documents(source_documents)
                    
                    # Combine the result and formatted sources
                    result_to_show = f"{result}\n\n\n### Source Documents:\n{formatted_sources}"
                    
                    st.chat_message('assistant').markdown(result_to_show)
                    
                    # Display any tables or charts that were extracted
                    if table_data:
                        st.chat_message('assistant').markdown("### Extracted Tables and Charts:")
                        for df, title in table_data:
                            display_table_or_chart(df, title)
                    
                    st.session_state.messages.append({'role':'assistant', 'content': result_to_show})
                    
                    # Add feedback buttons
                    col1, col2, col3 = st.columns([1, 1, 3])
                    with col1:
                        if st.button("👍 Helpful"):
                            st.success("Thank you for your feedback!")
                    with col2:
                        if st.button("👎 Not Helpful"):
                            st.error("We'll try to improve!")

            except Exception as e:
                st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()