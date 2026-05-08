from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from .loaders import LoadedDocument


def chunk_document(
    doc: LoadedDocument,
    *,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> Iterable[dict]:
    text = doc.text.strip()
    if not text:
        return

    start = 0
    index = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end].strip()
        if chunk_text:
            yield {
                "id": f"{doc.file_name}:{index}",
                "text": chunk_text,
                "metadata": {
                    **asdict(doc),
                    "project": "Winnipeg",
                    "chunk_index": index,
                },
            }
        if end == len(text):
            break
        start = max(0, end - overlap)
        index += 1

