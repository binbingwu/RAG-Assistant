# RAG Assistant

Independent local RAG assistant for project documentation.

This project is currently configured for Winnipeg project documents stored outside the code repository:

```text
C:\Users\bwu\
```

The raw documents stay outside this code project. The app reads them, creates a local vector index under `storage/`, retrieves relevant chunks locally, then sends only the selected chunks plus the user question to the DeepSeek API.

## What This App Does

```text
Project documents
  -> text extraction
  -> basic cleaning
  -> chunking
  -> local embeddings
  -> local vector index
  -> question-time retrieval
  -> DeepSeek API answer generation
  -> answer with retrieved sources
```

## Repository Safety

This repository should contain code only.

Do not commit:

- `.env`
- `storage/`
- `.venv/`
- `__pycache__/`
- raw company documents
- invoices, pricing, payroll, banking, or tax files

The `.gitignore` is configured to exclude local secrets, generated indexes, virtual environments, and Python cache files.

## Requirements

1. Install Python 3.11 or newer.
2. Have access to a DeepSeek API key.
3. Keep your source documents in a local folder outside the repository.

## 1. Create And Activate A Virtual Environment

```powershell
cd "C:\Users\bwu\OneDrive - Metercor Inc\Attachments\Desktop\RAG\winnipeg-rag-app"
python -m venv .venv
```

If PowerShell blocks activation scripts, allow scripts for the current terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of the terminal prompt.

## 2. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The main dependencies are:

- `sentence-transformers` for local embeddings
- `pypdf` for PDF text extraction
- `python-docx` for Word files
- `python-pptx` for PowerPoint files
- `openpyxl` for Excel files
- `beautifulsoup4` for HTML files
- `requests` for the DeepSeek API call
- `streamlit` for the optional web UI

## 3. Configure Environment Variables

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
notepad .env
```

Fill in:

```env
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_API_BASE=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat

RAG_SOURCE_DIR=C:\Users\bwu\OneDrive - Metercor Inc\Attachments\Desktop\RAG\Winnipeg documentation
RAG_STORAGE_DIR=storage
RAG_TOP_K=6
```

`RAG_SOURCE_DIR` points to your local document folder. The app reads from that folder but does not modify or copy the raw documents.

## 4. Build The Local RAG Index

```powershell
python -m src.ingest
```

The ingest command performs this pipeline:

```text
Read supported files
  -> extract text
  -> normalize whitespace and remove blank lines
  -> split long text into overlapping chunks
  -> create local embeddings
  -> save chunks and embeddings locally
```

It creates:

```text
storage/chunks.jsonl
storage/embeddings.npy
storage/manifest.json
```

These files are generated artifacts and are intentionally ignored by Git.

## 5. Ask Questions From The Command Line

```powershell
python -m src.chat "What is the Winnipeg deployment plan?"
```

Or interactive mode:

```powershell
python -m src.chat
```

In interactive mode:

```text
Winnipeg RAG chat. Type 'exit' to quit.

Question>
```

Type a question and press Enter. Type `exit` or `quit` to stop.

At question time, the app:

```text
Converts the question to an embedding
  -> searches the local vector index
  -> retrieves the top matching chunks
  -> sends question + retrieved chunks to DeepSeek
  -> prints the answer and retrieved sources
```

## 6. Optional Web UI

```powershell
streamlit run app.py
```

This opens a small local browser UI for asking questions.

## Supported Files

- `.pdf`
- `.docx`
- `.pptx`
- `.xlsx`
- `.txt`, `.md`, `.csv`, `.json`, `.js`, `.html`

PNG files are listed during ingest but are not OCR'd by default. Add OCR later only if screenshots contain important text.

## How Chunking Works

Chunking is implemented in `src/chunker.py`.

Default settings:

```text
chunk_size = 1200 characters
overlap = 200 characters
```

Example:

```text
Chunk 1: characters 0-1200
Chunk 2: characters 1000-2200
Chunk 3: characters 2000-3200
```

The overlap helps preserve context when a sentence or procedure crosses a chunk boundary.

## How Cleaning Works

Basic text cleaning is implemented in `src/loaders.py`.

The current cleaning step:

- normalizes line breaks
- trims whitespace
- removes blank lines

This is intentionally simple for the first version. Future improvements can include header/footer removal, duplicate removal, OCR, table cleanup, and sensitive-data redaction.

## How Embeddings Work

Embeddings are implemented in `src/embeddings.py`.

The default local embedding model is:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Each text chunk becomes a numeric vector. The vectors are normalized, so the app can use dot product as cosine similarity during retrieval.

## How The Local Vector Index Works

The local vector index is implemented in `src/index_store.py`.

It stores:

```text
chunks.jsonl       text chunks and metadata
embeddings.npy    local embedding matrix
manifest.json     ingest summary
```

Retrieval works by:

```text
question embedding
  -> dot product against all chunk embeddings
  -> sort by similarity score
  -> return top K chunks
```

This simple NumPy index is good for a small first version. For larger projects, consider replacing it with Qdrant, Chroma, FAISS, or PostgreSQL with pgvector.

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── .env.example
└── src
    ├── chat.py
    ├── chunker.py
    ├── config.py
    ├── deepseek_client.py
    ├── embeddings.py
    ├── index_store.py
    ├── ingest.py
    ├── loaders.py
    └── rag.py
```

## Privacy Note

This is not fully offline because answer generation uses DeepSeek API. The local index stays on your machine, but retrieved document snippets are sent to DeepSeek during chat. Do not index invoices, pricing, bank details, payroll, or other sensitive financial documents unless you accept that risk or switch generation to a fully local model.

## Publishing To GitHub

Before pushing, verify that generated and private files are ignored:

```powershell
git status --short --ignored
```

Only code and documentation should be committed. `storage/`, `.env`, `.venv/`, and raw source documents should remain untracked or ignored.
