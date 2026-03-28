# 🤖 RAG System Engineering Documentation

This document provides a comprehensive technical overview of the **Retrieval-Augmented Generation (RAG)** system for intelligent document processing and querying.

---

## 1. Project Overview and Purpose
The **RAG System** is an end-to-end pipeline designed to ingest, process, and query various document formats (PDF, Text, CSV, Excel, Word, JSON). It leverages semantic search and Large Language Models (LLMs) to provide accurate, context-aware answers to user queries based on a private knowledge base.

**Key Goals:**
- **Information Retrieval:** Efficiently find relevant document sections using vector embeddings.
- **Context-Aware Generation:** Use retrieved context to generate grounded responses via Groq-hosted LLMs.
- **Multi-Format Support:** Handle a wide range of document types seamlessly.

---

## 2. Architecture and Data Flow

### Technical Architecture Diagram
```text
+---------------------+       +----------------------+       +-----------------------+
|    Data Layer       |       |   Processing Layer   |       |    Storage Layer      |
|                     |       |                      |       |                       |
| [PDF][TXT][CSV]     | ----> | [Document Loaders]   | ----> | [FAISS Vector Index]  |
| [DOCX][XLSX][JSON]  |       | [Text Splitter]      |       | [Metadata (PKL)]      |
|                     |       | [Embedding Model]    |       |                       |
+---------------------+       +----------------------+       +-----------------------+
                                                                         |
                                                                         v
+---------------------+       +----------------------+       +-----------------------+
|  Generation Layer   |       |     Query Layer      |       |    Search Engine      |
|                     |       |                      |       |                       |
| [Groq LLM] <--------|-------| [Context Assembly]   | <---- | [Similarity Search]   |
| [Final Answer]      |       | [Query Embedding]    |       | [Top-K Retrieval]     |
+---------------------+       +----------------------+       +-----------------------+
```

### Data Flow Pipeline
1.  **Ingestion:** Files are scanned from the `data/` directory and loaded using format-specific LangChain loaders.
2.  **Chunking:** Documents are split into overlapping segments (default 1000 chars) using `RecursiveCharacterTextSplitter`.
3.  **Embedding:** Text chunks are converted into 384-dimensional vectors using the `all-MiniLM-L6-v2` model.
4.  **Indexing:** Vectors are stored in a FAISS L2 index for high-performance similarity search.
5.  **Retrieval:** User queries are embedded and compared against the FAISS index to find the most relevant chunks.
6.  **Synthesis:** Retrieved chunks are injected into a prompt and sent to Groq's LLM (`llama-3.1-8b-instant`) for final answer generation.

---

## 3. Tech Stack and Dependencies

### Core Libraries
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | LangChain | RAG pipeline and document management |
| **LLM Provider** | Groq | High-speed inference for Llama models |
| **Embeddings** | Sentence Transformers | Vectorizing text (all-MiniLM-L6-v2) |
| **Vector DB** | FAISS | Efficient similarity search on disk |
| **Parsers** | PyMuPDF, pypdf, docx2txt | Multi-format document parsing |

### External Dependencies
- **Groq API Key:** Required for response generation (`GROQ_API_KEY`).
- **Python 3.13+:** Runtime environment.

---

## 4. Folder Structure

```
rag/
├── data/                  # Input documents (PDF, TXT, etc.)
│   └── vector_store/      # Optional ChromaDB storage
├── src/                   # Core source code
│   ├── data_loader.py     # Multi-format document loading logic
│   ├── embedding.py       # Text chunking and embedding pipeline
│   ├── vector_store.py    # FAISS index management (save/load/query)
│   └── search.py          # RAG orchestration and LLM integration
├── faiss_store/           # Persistent FAISS index and metadata
├── notebook/              # Jupyter notebooks for experimentation
├── app.py                 # Example programmatic entry point
├── main.py                # CLI tool for interactive search
└── pyproject.toml         # Dependency and project configuration
```

---

## 5. Setup and Usage

### Initialization
1.  **Environment:** Create a `.env` file in the root directory:
    ```env
    GROQ_API_KEY=your_api_key_here
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Running Development
- **Interactive CLI:**
  ```bash
  python main.py
  ```
- **Single Query:**
  ```bash
  python main.py "How does the attention mechanism work?" --top-k 5
  ```

### Production Considerations
- Ensure `faiss_store/` is persistent across deployments.
- Use a robust environment manager like `uv` (as indicated by `uv.lock`).

---

## 6. Extending and Modifying

### Adding New Document Types
Modify `src/data_loader.py` within the `Load_all_documents` function to include new loaders from `langchain_community.document_loaders`.

### Changing Embedding Models
Update the `embedding_model` parameter in `FaissVectorStore` or `EmbeddingGenerator` (`src/embedding.py`). Note that changing the model requires rebuilding the FAISS index.

### Custom Prompting
Edit `src/search.py` in the `search_summarize` method to adjust the system prompt or temperature settings for the LLM.

---

## 7. Sample Usage Workflow

**Scenario: Querying Corporate Notes**
1.  Place `Q3_Report.pdf` in `data/pdf/`.
2.  Run `python main.py`.
3.  The system will:
    - Detect the new file and rebuild/update the index.
    - Ask for your question.
    - **User:** "What was the revenue growth?"
    - **System:** "Based on the Q3 Report (page 4), revenue grew by 12% year-over-year..."

---

## 8. Testing Strategy
Currently, the project includes `pytest` as a development dependency in `pyproject.toml`. 
- **To Run Tests (Once created):** `pytest`
- **Recommended Tests:**
    - `tests/test_loader.py`: Verify document parsing for all 6 supported formats.
    - `tests/test_vector_store.py`: Ensure FAISS save/load integrity.
    - `tests/test_rag.py`: Mock Groq API to test context injection.

---

## 9. Performance and Security

### Performance
- **FAISS:** Uses FlatL2 index, providing sub-10ms retrieval times for small-to-medium datasets.
- **Groq:** Offers near-instantaneous token generation compared to local LLMs.

### Security
- **API Keys:** Sensitive keys are managed via `.env` and `load_dotenv()`. Never commit `.env` to source control.
- **Local Data:** Documents stay on your local machine; only the retrieved text chunks and the query are sent to the Groq API.
