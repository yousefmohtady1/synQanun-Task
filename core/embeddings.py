import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from config.settings import settings

class EmbeddingModel:
    def __init__(self):
        print(f"Loading embedding model: {settings.EMBEDDINGS_MODEL}")
        self.model = SentenceTransformer(settings.EMBEDDINGS_MODEL)

        self.model.max_seq_length = 8192
        
    def embed_documents(self, texts: List[str]) ->np.ndarray:
        
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
            batch_size=4
        )
        return embeddings
    
    def embed_query(self, query: str) -> np.ndarray:
        
        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding[0]