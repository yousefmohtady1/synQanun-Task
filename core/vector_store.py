import chromadb
import uuid
from typing import List, Dict
from config.settings import settings
from .chunking import DocumentChunk
from .embeddings import EmbeddingModel

class VectorStore:
    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model
        self.client = chromadb.PersistentClient(path = settings.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name = settings.COLLECTION_NAME)
        
    def index_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            return
        
        print(f"Embedding {len(chunks)} chunks...")
        
        ids = [str(uuid.uuid4()) for _ in chunks]
        
        texts = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        
        embeddings_np = self.embedding_model.embed_documents(texts)
        embeddings_list = embeddings_np.tolist()
        
        self.collection.add(
            ids = ids,
            embeddings = embeddings_list,
            documents = texts,
            metadatas = metadatas
        )
        
        print(f"Successfully stored {len(chunks)} chunks.")

    def search(self, query:str, top_k:int=5) -> List[Dict]:
        
        query_vector_np = self.embedding_model.embed_query(query)
        query_vector_list = query_vector_np.tolist()
        
        results = self.collection.query(
            query_embeddings = [query_vector_list],
            n_results = top_k
        )

        formatted_results = []
        if results['ids'] and results['ids'][0]:
            count = len(results['ids'][0])
            for i in range(count):
                formatted_results.append({
                    "score" : 1 - results['distances'][0][i],
                    "content" : results['documents'][0][i],
                    "metadata" : results['metadatas'][0][i]
                })
                
        return formatted_results