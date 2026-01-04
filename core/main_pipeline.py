import os
from typing import List, Dict
from config.settings import settings
from .embeddings import EmbeddingModel
from .vector_store import VectorStore
from .data_pipeline import DataPipeline

class SearchPipeline:
    def __init__(self):
        self.vector_store = None
        self._initialize()
    
    def _initialize(self):
        db_exists = False
        if os.path.exists(settings.CHROMA_DB_DIR):
            if len(os.listdir(settings.CHROMA_DB_DIR)) > 0:
                db_exists = True
                
        if not db_exists:
            print("Database not found. Triggering Auto-Ingestion")
            pipeline = DataPipeline()
            pipeline.run()
            
        print("Conncting to vector store")
        embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(embedding_model)
        print("search pipeline is ready")
        
    def search(self, query : str, top_k : int = 5):
        if not self.vector_store:
            raise Exception("Pipeline not initialized.")
        
        results= self.vector_store.search(query, top_k)
        return {
            "query" : query,
            "count" : len(results),
            "results" : results
        }