import time
from .chunking import Chunker
from .embeddings import EmbeddingModel
from .vector_store import VectorStore

class DataPipeline:
    def run(self):
        print("Starting Data Ingestion Pipeline...")
        start_time = time.time()
        
        print("\n[1/3] Loading and Chunking Documents...")
        chunker = Chunker()
        chunks = chunker.load_and_chunk()
        
        if not chunks:
            print("No chunks generated. Please check your 'data' folder.")
            return
        
        print("\n[2/3] Initializing Models & Indexing...")
        embedding_model = EmbeddingModel()
        vector_store = VectorStore(embedding_model)
        vector_store.index_chunks(chunks)
        
        print("\n[3/3] Saving Artifacts...")
        vector_store.save()
        end_time = time.time()
        print(f"\nPipeline finished successfully in {end_time - start_time:.2f} seconds")