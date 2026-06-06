import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pageindex import PageIndexClient
from ingestion.batch_ingestor import run as run_ingestion
from utils import load_registry

load_dotenv()

pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))
app = FastAPI(title="Multimodal RAG API")


class QueryRequest(BaseModel):
    query: str


@app.post("/ingest")
def ingest():
    try:
        return run_ingestion()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query(request: QueryRequest):
    try:
        registry = load_registry()
        if not registry:
            raise HTTPException(status_code=400, detail="No documents ingested yet.")

        doc_ids = list(registry.values())

        response = pi_client.chat_completions(
            messages=[{"role": "user", "content": request.query}],
            doc_id=doc_ids,
            enable_citations=True,
        )

        answer = response["choices"][0]["message"]["content"]
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))