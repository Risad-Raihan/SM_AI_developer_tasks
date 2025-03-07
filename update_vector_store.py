from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
import logging
import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths
DATA_PATH = "data/"
DB_FAISS_PATH = "vectorstore/db_faiss"
NEW_PDF_FILE = "DavidsonMedicine24th.pdf"

def load_specific_pdf(pdf_file_path):
    """Load a specific PDF file and convert it to Document objects."""
    try:
        documents = []
        
        with open(pdf_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            pdf_file = os.path.basename(pdf_file_path)
            logger.info(f"PDF file '{pdf_file}' has {num_pages} pages")
            
            # Extract text from each page
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                # Create a Document object with metadata
                doc = Document(
                    page_content=text,
                    metadata={"source": pdf_file, "page": page_num + 1}
                )
                documents.append(doc)
        
        return documents
    except Exception as e:
        logger.error(f"Error loading PDF: {str(e)}")
        return []

def create_chunks(extracted_data):
    """Create chunks of text from the extracted data."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def get_embedding_model():
    """Get the embedding model."""
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedding_model

def update_vector_store():
    """Update the existing vector store with new PDF data."""
    try:
        # Step 1: Load the new PDF file
        pdf_path = os.path.join(DATA_PATH, NEW_PDF_FILE)
        logger.info(f"Loading PDF from {pdf_path}")
        documents = load_specific_pdf(pdf_path)
        logger.info(f"Loaded {len(documents)} pages from the PDF")
        
        if not documents:
            logger.error("No documents loaded from the PDF")
            return
        
        # Step 2: Create chunks of text
        logger.info("Creating text chunks...")
        text_chunks = create_chunks(documents)
        logger.info(f"Created {len(text_chunks)} chunks from the PDF")
        
        # Step 3: Get the embedding model
        logger.info("Loading embedding model...")
        embedding_model = get_embedding_model()
        
        # Step 4: Load the existing vector store
        logger.info(f"Loading existing vector store from {DB_FAISS_PATH}")
        try:
            existing_db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
            logger.info("Successfully loaded existing vector store")
        except Exception as e:
            logger.error(f"Error loading existing vector store: {str(e)}")
            logger.info("Creating a new vector store instead")
            existing_db = None
        
        # Step 5: Add the new chunks to the vector store
        logger.info("Adding new chunks to the vector store...")
        if existing_db:
            existing_db.add_documents(text_chunks)
            existing_db.save_local(DB_FAISS_PATH)
            logger.info(f"Updated vector store saved to {DB_FAISS_PATH}")
        else:
            new_db = FAISS.from_documents(text_chunks, embedding_model)
            new_db.save_local(DB_FAISS_PATH)
            logger.info(f"New vector store saved to {DB_FAISS_PATH}")
        
        logger.info("Vector store update completed successfully")
    
    except Exception as e:
        logger.error(f"Error updating vector store: {str(e)}")

if __name__ == "__main__":
    update_vector_store() 