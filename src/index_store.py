from __future__ import annotations

import json
from pathlib import Path

import numpy as np


class LocalVectorIndex:
    def __init__(self, storage_dir: Path) -> None:
        self.storage_dir = storage_dir
        self.chunks_path = storage_dir / "chunks.jsonl"
        self.embeddings_path = storage_dir / "embeddings.npy"

    def save(self, chunks: list[dict], embeddings: np.ndarray) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        with self.chunks_path.open("w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        np.save(self.embeddings_path, embeddings)

    def load(self) -> tuple[list[dict], np.ndarray]:
        if not self.chunks_path.exists() or not self.embeddings_path.exists():
            raise FileNotFoundError("Index not found. Run: python -m src.ingest")

        chunks = []
        with self.chunks_path.open("r", encoding="utf-8") as f:
            for line in f:
                chunks.append(json.loads(line))
        embeddings = np.load(self.embeddings_path)
        return chunks, embeddings

    @staticmethod
    def search(
        query_embedding: np.ndarray,
        chunks: list[dict],
        embeddings: np.ndarray,
        *,
        top_k: int,
    ) -> list[dict]:
        scores = embeddings @ query_embedding.reshape(-1)
        best_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in best_indices:
            item = dict(chunks[int(idx)])
            item["score"] = float(scores[int(idx)])
            results.append(item)
        return results

