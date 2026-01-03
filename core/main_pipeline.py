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
        index_path = os.path.join(settings.ARTIFACTS_DIR, "index.faiss")
        
        if not os.path.exists(index_path):
            print ("Artifacts not found. Triggering Auto-Ingestion Pipeline...")
            ingestion_worker = DataPipeline()
            ingestion_worker.run()
            
        print("Loading Vector Store...")
        embedding_model = EmbeddingModel()
        self.vector_store = VectorStore(embedding_model)
        self.vector_store.load()
        print("Search Pipeline Ready.")
        
    def search(self, query : str, top_k : int = 5):
        if not self.vector_store:
            raise Exception("Pipeline not initialized.")
        
        results= self.vector_store.search(query, top_k)
        return {
            "query" : query,
            "count" : len(results),
            "results" : results
        }