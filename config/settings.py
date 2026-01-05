import os

class Settings:
    # Model
    EMBEDDINGS_MODEL = "BAAI/bge-m3"
    
    # Data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    LAWS_DIR = os.path.join(DATA_DIR, "laws")
    JUDGMENTS_DIR = os.path.join(DATA_DIR, "judgments")
    FATWAS_DIR = os.path.join(DATA_DIR, "fatwas")
    
    # Vector Database
    CHROMA_DB_DIR = os.path.join(BASE_DIR, "chroma_storage")
    COLLECTION_NAME = "legal_docs"
    
    # Chunking
    CHUNK_SIZE = 2000

settings = Settings()