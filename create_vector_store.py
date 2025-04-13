import json
from typing import List, Dict
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

def load_restaurant_data(file_path: str) -> Dict:
    """Load the restaurant dataset from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_documents_from_data(data: Dict) -> List[Document]:
    """Convert restaurant data into Langchain documents."""
    documents = []
    
    # Process restaurant information
    restaurant = data.get('restaurant', {})
    content = f"Restaurant Name: {restaurant.get('name', '')}\n"
    content += f"About: {restaurant.get('about', '')}\n"
    content += f"Address: {restaurant.get('address', {}).get('street', '')}, "
    content += f"{restaurant.get('address', {}).get('city', '')}, "
    content += f"{restaurant.get('address', {}).get('state', '')} "
    content += f"{restaurant.get('address', {}).get('zip', '')}\n"
    content += f"Phone: {restaurant.get('contact', {}).get('phone', '')}\n"
    content += f"Email: {restaurant.get('contact', {}).get('email', '')}\n"
    content += f"Website: {restaurant.get('contact', {}).get('website', '')}\n"
    content += "Opening Hours:\n"
    for day, hours in restaurant.get('hours', {}).items():
        content += f"{day}: {hours.get('open', '')} - {hours.get('close', '')}\n"
    content += f"Cuisine Types: {', '.join(restaurant.get('cuisine_types', []))}\n"
    content += f"Features: {', '.join(restaurant.get('features', []))}\n"
    documents.append(Document(page_content=content, metadata={"type": "restaurant_info"}))
    
    # Process menu items
    for category in data.get('menu', {}).get('categories', []):
        category_name = category.get('name', '')
        category_desc = category.get('description', '')
        
        for item in category.get('items', []):
            content = f"Menu Item: {item.get('name', '')}\n"
            content += f"Category: {category_name}\n"
            content += f"Category Description: {category_desc}\n"
            content += f"Description: {item.get('description', '')}\n"
            content += f"Price: ${item.get('price', 0):.2f}\n"
            
            # Add dietary information
            dietary_tags = []
            if item.get('vegetarian'):
                dietary_tags.append('vegetarian')
            if item.get('vegan'):
                dietary_tags.append('vegan')
            if item.get('gluten_free'):
                dietary_tags.append('gluten-free')
            
            if dietary_tags:
                content += f"Dietary Tags: {', '.join(dietary_tags)}\n"
            
            if item.get('calories'):
                content += f"Calories: {item.get('calories')}\n"
            
            if item.get('popular'):
                content += "Popular Item: Yes\n"
            
            if item.get('chef_recommended'):
                content += "Chef's Recommendation: Yes\n"
            
            documents.append(Document(page_content=content, metadata={"type": "menu_item"}))
    
    # Process special events and promotions
    specials = data.get('menu', {}).get('specials', {})
    
    # Happy Hour
    happy_hour = specials.get('happy_hour', {})
    if happy_hour:
        content = "Happy Hour Specials:\n"
        content += f"Times: {happy_hour.get('times', '')}\n"
        content += f"Days: {', '.join(happy_hour.get('days', []))}\n"
        content += "Offers:\n"
        for offer in happy_hour.get('offers', []):
            content += f"- {offer}\n"
        documents.append(Document(page_content=content, metadata={"type": "special_event"}))
    
    # Weekly Specials
    for special in specials.get('weekly_specials', []):
        content = f"Special Event: {special.get('name', '')}\n"
        content += f"Description: {special.get('description', '')}\n"
        content += f"Valid Days: {', '.join(special.get('valid_days', []))}\n"
        documents.append(Document(page_content=content, metadata={"type": "special_event"}))
    
    return documents

def main():
    # Load the restaurant data
    data_path = "data/res-bot-dataset.json"
    restaurant_data = load_restaurant_data(data_path)
    
    # Create documents
    documents = create_documents_from_data(restaurant_data)
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Split documents
    split_docs = text_splitter.split_documents(documents)
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create vector store
    vector_store_path = "vectorstore/db_faiss"
    os.makedirs(vector_store_path, exist_ok=True)
    
    vector_store = FAISS.from_documents(
        documents=split_docs,
        embedding=embeddings
    )
    
    # Save vector store
    vector_store.save_local(vector_store_path)
    print(f"Vector store created and saved to {vector_store_path}")
    print(f"Total documents processed: {len(split_docs)}")

if __name__ == "__main__":
    main() 