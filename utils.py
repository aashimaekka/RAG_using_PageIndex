import json
import os
from dotenv import load_dotenv

load_dotenv()
DOC_REGISTRY = os.getenv("DOC_REGISTRY")


def load_registry() -> dict:
    if os.path.exists(DOC_REGISTRY):
        with open(DOC_REGISTRY, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)
    return {}


def save_registry(registry: dict):
    with open(DOC_REGISTRY, "w") as f:
        json.dump(registry, f, indent=2)


def invert_registry(registry: dict) -> dict:
    return {v: k for k, v in registry.items()}