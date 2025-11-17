import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 
PDF_PATH = os.getenv("PDF_PATH", "data")
VECTOR_DIR = os.getenv("VECTOR_DIR", "vectorstore")
TOP_K = int(os.getenv("TOP_K", "4"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800")) 
OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
