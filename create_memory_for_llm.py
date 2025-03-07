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

#step 1: Load raw pdf
DATA_PATH = "data/"
def load_pdf_files(data_path):
    try:
        pdf_files = [f for f in os.listdir(data_path) if f.endswith('.pdf')]
        documents = []
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(data_path, pdf_file)
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                print(f"PDF file '{pdf_file}' has {num_pages} pages")
                
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
        logger.error(f"Error loading PDFs: {str(e)}")
        return []

documents = load_pdf_files(data_path=DATA_PATH)
#print("\nTotal pages loaded: ", len(documents))

#step 2 : create chunks of text
def create_chunks(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = create_chunks(documents)
#print("\nTotal chunks created: ", len(text_chunks))



#step 3: create vector embeddings

def getembedding_model():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embedding_model

embedding_model = getembedding_model()


#step 4: store embeding in FAISS 
DB_FAISS_PATH = "vectorstore/db_faiss"

db = FAISS.from_documents(text_chunks, embedding_model)
db.save_local(DB_FAISS_PATH)





