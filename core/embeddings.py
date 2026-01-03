import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from config.settings import settings

class EmbeddingModel:
    def __init__(self):
        print(f"Loading embedding model: {settings.EMBEDDINGS_MODEL}")
        self.model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
        
    def embed_documents(self, texts: List[str]) ->np.ndarray:
        formatted_texts = [f"passage: {t}" for t in texts]
        
        embeddings = self.model.encode(
            formatted_texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=16
        )
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        formatted_query = f"query: {query}"
        
        embedding = self.model.encode(
            [formatted_query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding[0]