import os

class Settings:
    # Model
    EMBEDDINGS_MODEL = "intfloat/multilingual-e5-large"
    
    # Data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    LAWS_DIR = os.path.join(DATA_DIR, "laws")
    JUDGMENTS_DIR = os.path.join(DATA_DIR, "judgments")
    FATWAS_DIR = os.path.join(DATA_DIR, "fatwas")
    ARTIFACTS_DIR = os.path.join(BASE_DIR, "artifacts")
    
    # Chunking
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

settings = Settings()