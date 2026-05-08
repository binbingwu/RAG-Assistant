from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


DEFAULT_SOURCE_DIR = (
    r"C:\Users\bwu\OneDrive - Metercor Inc\Attachments\Desktop\RAG\Winnipeg documentation"
)


@dataclass(frozen=True)
class Settings:
    source_dir: Path
    storage_dir: Path
    api_key: str
    api_base: str
    model: str
    top_k: int
    embedding_model: str


def get_settings() -> Settings:
    return Settings(
        source_dir=Path(os.getenv("RAG_SOURCE_DIR", DEFAULT_SOURCE_DIR)),
        storage_dir=Path(os.getenv("RAG_STORAGE_DIR", "storage")),
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        api_base=os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com").rstrip("/"),
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        top_k=int(os.getenv("RAG_TOP_K", "6")),
        embedding_model=os.getenv(
            "RAG_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
        ),
    )

