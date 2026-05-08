from __future__ import annotations

import json
from datetime import datetime

from .chunker import chunk_document
from .config import get_settings
from .embeddings import LocalEmbedder
from .index_store import LocalVectorIndex
from .loaders import iter_supported_files, load_document


def main() -> None:
    settings = get_settings()
    if not settings.source_dir.exists():
        raise FileNotFoundError(f"Source directory does not exist: {settings.source_dir}")

    print(f"Reading documents from: {settings.source_dir}")
    documents = []
    skipped = []

    for path in iter_supported_files(settings.source_dir):
        try:
            doc = load_document(path)
            if doc.text.strip():
                documents.append(doc)
                print(f"Loaded: {path.name}")
            else:
                skipped.append({"path": str(path), "reason": "empty text"})
        except Exception as exc:
            skipped.append({"path": str(path), "reason": repr(exc)})
            print(f"Skipped: {path.name} ({exc})")

    chunks = []
    for doc in documents:
        chunks.extend(list(chunk_document(doc)))

    if not chunks:
        raise RuntimeError("No text chunks were created.")

    print(f"Created {len(chunks)} chunks. Building local embeddings...")
    embedder = LocalEmbedder(settings.embedding_model)
    embeddings = embedder.encode([chunk["text"] for chunk in chunks])

    index = LocalVectorIndex(settings.storage_dir)
    index.save(chunks, embeddings)

    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "source_dir": str(settings.source_dir),
        "embedding_model": settings.embedding_model,
        "document_count": len(documents),
        "chunk_count": len(chunks),
        "skipped": skipped,
    }
    settings.storage_dir.mkdir(parents=True, exist_ok=True)
    (settings.storage_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Index saved to: {settings.storage_dir}")


if __name__ == "__main__":
    main()

