# Multimodal RAG API

A local RAG application that lets you query multimodal PDFs using PageIndex and Gemini.

## Architecture

- **Ingestion**: Batch uploads PDFs from a local directory to PageIndex
- **Retrieval + Generation**: PageIndex Chat API handles reasoning-based retrieval; response includes inline citations
- **API**: FastAPI with Swagger UI

## Prerequisites

- Python 3.10+
- PageIndex API key → [dash.pageindex.ai/api-keys](https://dash.pageindex.ai/api-keys)
- Gemini API key → [aistudio.google.com](https://aistudio.google.com)

## Setup

1. **Clone and install dependencies**
```bash
   pip install -r requirements.txt
```

2. **Create `.env`**
```env
   GEMINI_API_KEY=your_gemini_key
   PAGEINDEX_API_KEY=your_pageindex_key
   INPUT_DIR=./data
   DOC_REGISTRY=./doc_registry.json
```

3. **Add PDFs**

Place your PDFs in the `./data` directory.

4. **Run the server**
```bash
   uvicorn main:app --reload
```

5. **Open Swagger UI**

Navigate to `http://localhost:8000/docs` to access the API documentation and test the endpoints.

## Usage

### 1. Ingest PDFs
`POST /ingest` — scans `./data` and uploads all PDFs to PageIndex.
- Already ingested files are skipped automatically.
- Re-run anytime you add new PDFs.

### 2. Query
`POST /query`
```json
{
  "query": "your question here"
}
```
Response includes inline citations in the format `<doc=filename.pdf;page=1>`.

## Project Structure

rag-app/
├── main.py                  # FastAPI app
├── utils.py                 # Registry helpers
├── ingestion/
│   └── batch_ingestor.py    # PDF ingestion pipeline
├── data/                    # Drop PDFs here
├── doc_registry.json        # Auto-generated, tracks ingested docs
├── .env                     # API keys and config
└── requirements.txt

## Notes

- PageIndex handles chunking, indexing, and retrieval internally — no vector DB needed
- `doc_registry.json` prevents re-ingestion of already uploaded files
- Gemini `gemini-2.5-pro` is used for generation (configurable in `orchestrator.py`)