# SynQanun Semantic Search

SynQanun is a semantic search engine designed for legal documents. It ingests laws, judgments, and fatwas, processes them into chunks, creates embeddings using `SentenceTransformers`, and stores them in a ChromaDB vector database for fast similarity search.

## Features

- **Document Ingestion**: Supports `.docx` files for Laws, Judgments, and Fatwas.
- **Smart Chunking**: Uses structure-aware chunking for articles and paragraph-aware chunking for general text.
- **Semantic Search**: Powered by `sentence-transformers` and `ChromaDB`.
- **API**: Provides a REST API using `FastAPI` to query the knowledge base.
- **Auto-Pipeline**: Automatically ingests and indexes data on startup if artifacts are missing.

## Project Structure

```
synQanun-Task/
├── app.py                 # FastAPI Application entry point
├── config/               
│   └── settings.py        # Project settings (paths, model names)
├── core/
│   ├── chunking.py        # Document parsing and chunking logic
│   ├── data_pipeline.py   # Orchestrates the ingestion process
│   ├── embeddings.py      # Embedding model wrapper
│   ├── main_pipeline.py   # Search service wrapper
│   └── vector_store.py    # ChromaDB vector store management
└── data/                  # Place your .docx files here
    ├── laws/
    ├── judgments/
    └── fatwas/
```

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd synQanun-Task
    ```

2.  **Install Dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    pip install -r requirements.txt
    ```

    *Note: Initializes `sentence-transformers` which might download the model (`intfloat/multilingual-e5-large`) on first run.*

## Usage

### 1. Prepare Data
Place your Word documents (`.docx`) in the appropriate folders under `data/`:
- `data/laws/`
- `data/judgments/`
- `data/fatwas/`

### 2. Run the Application
Start the API server:
```bash
python app.py
```
*Or directly with uvicorn:*
```bash
uvicorn app:app --reload
```

On the first run, the system will detect missing artifacts and run the ingestion pipeline automatically:
1.  Load and chunk documents.
2.  Generate embeddings.
3.  Store them in the ChromaDB collection.

### 3. API Documentation
Once running, access the automatic API docs at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### 4. Search Endpoint
**POST** `/search`

## Configuration
Adjust settings in `config/settings.py` to change directories, chunk sizes, or the embedding model.