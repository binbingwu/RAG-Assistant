from __future__ import annotations

import sys

from .rag import answer_question


def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:]).strip()
        _ask(question)
        return

    print("Winnipeg RAG chat. Type 'exit' to quit.")
    while True:
        question = input("\nQuestion> ").strip()
        if question.lower() in {"exit", "quit"}:
            break
        if question:
            _ask(question)


def _ask(question: str) -> None:
    answer, sources = answer_question(question)
    print("\nAnswer:\n")
    print(answer)
    print("\nRetrieved sources:")
    for source in sources:
        meta = source["metadata"]
        print(f"- {meta['file_name']} | chunk {meta['chunk_index']} | score {source['score']:.3f}")


if __name__ == "__main__":
    main()

