import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pageindex import PageIndexClient
from utils import load_registry, save_registry

load_dotenv()

pi_client = PageIndexClient(api_key=os.getenv("PAGEINDEX_API_KEY"))
INPUT_DIR = os.getenv("INPUT_DIR")


def poll_until_ready(doc_id: str, timeout: int = 300, interval: int = 5) -> bool:
    elapsed = 0
    while elapsed < timeout:
        status = pi_client.get_document(doc_id).get("status")
        if status == "completed":
            return True
        if status == "failed":
            return False
        time.sleep(interval)
        elapsed += interval
    return False


def run() -> dict:
    registry = load_registry()
    results = {"submitted": [], "skipped": [], "failed": []}

    pdf_files = list(Path(INPUT_DIR).glob("*.pdf"))
    if not pdf_files:
        return {"message": "No PDF files found", **results}

    for pdf_path in pdf_files:
        filename = pdf_path.name

        if filename in registry:
            results["skipped"].append(filename)
            continue

        try:
            result = pi_client.submit_document(str(pdf_path))
            doc_id = result["doc_id"]

            ready = poll_until_ready(doc_id)
            if ready:
                registry[filename] = doc_id
                save_registry(registry)
                results["submitted"].append(filename)
            else:
                results["failed"].append(filename)
        except Exception as e:
            results["failed"].append(f"{filename}: {str(e)}")

    return results