from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('HF_TOKEN')
print(f'HuggingFace token exists: {bool(token)}')
if token:
    print(f'Token starts with: {token[:8]}...') 