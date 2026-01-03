import uvicorn
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from core.main_pipeline import SearchPipeline

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

app = FastAPI(
    title = "SynQanun Semantic Search"
)

search_service = None

@app.on_event("startup")
async def startup_event():
    global search_service
    try:
        search_service = SearchPipeline()
    except Exception as e:
        print(f"Failed to initialize search service: {e}")

@app.get("/")
def home():
    return {"status" : "Online", "message" : "Legal Search API is Running."}

@app.post("/search")
def search_endpoint(request: SearchRequest):
    
    global search_service
    if not search_service:
        raise HTTPException(status_code = 503, detail = "Search service is initializing...")
    
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        response = search_service.search(request.query, request.top_k)
        return response
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
if __name__ == "__main__":
    uvicorn.run("app:app", reload = True)