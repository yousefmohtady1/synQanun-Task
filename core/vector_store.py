import os
import pickle
import numpy as np
import faiss
from typing import List, Dict
from config.settings import settings
from .chunking import DocumentChunk
from .embeddings import EmbeddingModel

class VectorStore:
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model
        self.index = None
        self.metadata_store = []
        
    def index_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            print("No chunks to index.")
            return
        
        print(f"Embedding {len(chunks)} chunks...")
        
        texts = [chunk.content for chunk in chunks]
        
        embeddings = self.embedding_model.embed_documents(texts)
        dimension = embeddings.shape[1]
        
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)
        
        self.chunks_data = chunks
        
        print(f"Indexed {len(chunks)} vectors of dimension {dimension}.")

    def search(self, query:str, top_k:int=5) -> List[Dict]:
        if self.index is None:
            raise Exception("Index is empty. Load or build it first.")
        
        query_vector = self.embedding_model.embed_query(query)
        query_vector = query_vector.reshape(1, -1)
        
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for i in range(top_k):
            idx = indices[0][i]
            score = scores[0][i]
            
            if idx != -1:
                chunk = self.chunks_data[idx]
                results.append({
                    "score": float(score),
                    "content": chunk.content,
                    "metadata": chunk.metadata
                })
        return results
    
    def save(self):
        if not os.path.exists(settings.ARTIFACTS_DIR):
            os.makedirs(settings.ARTIFACTS_DIR)
        
        index_path = os.path.join(settings.ARTIFACTS_DIR, "index.faiss")
        data_path = os.path.join(settings.ARTIFACTS_DIR, "chunks.pkl")
        
        faiss.write_index(self.index, index_path)
        with open(data_path, "wb") as f:
            pickle.dump(self.chunks_data, f)
         
        print(f"Vector store saved to {settings.ARTIFACTS_DIR}")
    
    def load(self):
        index_path = os.path.join(settings.ARTIFACTS_DIR, "index.faiss")
        data_path = os.path.join(settings.ARTIFACTS_DIR, "chunks.pkl")
        
        if not os.path.exists(index_path) or not os.path.exists(data_path):
            raise FileNotFoundError("Artifacts not found. Please ensure the vector store has been saved.")
        
        self.index = faiss.read_index(index_path)
        with open(data_path, "rb") as f:
            self.chunks_data = pickle.load(f)
        
        print(f"Loaded vector store from {settings.ARTIFACTS_DIR}")