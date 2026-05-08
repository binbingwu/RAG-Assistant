from __future__ import annotations

from .config import get_settings
from .deepseek_client import DeepSeekClient
from .embeddings import LocalEmbedder
from .index_store import LocalVectorIndex


SYSTEM_PROMPT = """You are Metercor's internal Winnipeg project assistant.
Answer only from the provided retrieved context.
If the context does not contain the answer, say you cannot find it in the Winnipeg documentation.
Do not invent facts. Keep answers practical and concise.
Always include a Sources section using the provided file names."""


def answer_question(question: str) -> tuple[str, list[dict]]:
    settings = get_settings()
    index = LocalVectorIndex(settings.storage_dir)
    chunks, embeddings = index.load()

    embedder = LocalEmbedder(settings.embedding_model)
    query_embedding = embedder.encode([question])[0]
    retrieved = index.search(
        query_embedding,
        chunks,
        embeddings,
        top_k=settings.top_k,
    )

    context = _format_context(retrieved)
    client = DeepSeekClient(
        api_key=settings.api_key,
        api_base=settings.api_base,
        model=settings.model,
    )
    answer = client.chat(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question:\n{question}\n\nRetrieved context:\n{context}",
            },
        ]
    )
    return answer, retrieved


def _format_context(chunks: list[dict]) -> str:
    parts = []
    for idx, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]
        parts.append(
            "\n".join(
                [
                    f"[Source {idx}]",
                    f"File: {metadata['file_name']}",
                    f"Path: {metadata['path']}",
                    f"Chunk: {metadata['chunk_index']}",
                    f"Score: {chunk['score']:.4f}",
                    "Text:",
                    chunk["text"],
                ]
            )
        )
    return "\n\n---\n\n".join(parts)

