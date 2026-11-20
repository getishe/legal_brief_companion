# Legal Brief Companion - RAG-Powered Legal and Technical Assistant

This project implements a modular Retrieval-Augmented Generation (RAG) assistant using LangChain, designed to answer legal and technical queries based on custom documents. It features document ingestion, semantic retrieval, prompt templating, and LLM-backed response generation—all wrapped in a clean CLI and Streamlit interface.

## Project Structure as follows

```text
legal_brief_companion/
├── src/
│   └── legal_brief_companion/
│       ├── __init__.py
│       ├── config/
│       │   └── settings.py           # Application configuration and env loading
│       ├── ingestion/
│       │   ├── document_loader.py    # Load PDFs/texts into the pipeline
│       │   └── text_splitter.py      # Chunk large documents
│       ├── retrieval/
│       │   ├── vector_store.py       # Manage vector store persistence (Chroma)
│       │   └── retriever.py          # Query and rank relevant chunks
│       ├── llm/
│       │   ├── chain.py              # LLM orchestration and chains
│       │   └── prompt_templates.py   # Reusable prompt templates
│       ├── interface/
│       │   └── cli.py                # CLI for local usage
│       ├── utils/
│       │   └── helpers.py            # Shared utilities and helpers
│       └── tests/                        # Unit tests
│       |     ├── test_chain.py
│       |     ├── test_ingestion.py
│       |     └── test_llm.py
│       └── ingest.py                 # CLI/script entry for ingestion
├── data/
│   ├── documents/                    # User documents (PDFs, txt)
│   └── vector_store/                 # Persisted vector DB files
│       └── <instance-id>/
|
├── app.py                            # Streamlit / main app entry
├── pyproject.toml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Groq API key
- pip or poetry

## ⚙️ Setup Instructions

1.  Clone the repository:

    ```bash
    git clone <your_repository_url>
    cd legal_brief_companion
    ```

2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3.  Set up your environment variables in the `.env` file. **Important:** Do not hardcode your API key directly in the `.env` file. Instead, set it as an environment variable in your system.

    ```
    GROQ_API_KEY=your_groq_key
    EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
    LLM_PROVIDER=groq
    LLM_MODEL=openai/gpt-oss-20b
    DATABASE_URL=sqlite:///data/knowledge_base.db
    DOCUMENTS_PATH=data/documents
    PERSIST_DIRECTORY=data/vector_store
    MODEL_NAME=openai/gpt-oss-20b
    VECTOR_STORE_TYPE=chroma

    debug = true
    ```

4.  Set your Groq API key as an environment variable:

    ```bash
    # PowerShell
    $env:GROQ_API_KEY="your_api_key_here"

    # Linux/macOS
    export GROQ_API_KEY="your_api_key_here"
    ```

5.  Ingest your documents: This process splits and indexes the documents in the vector store.

    ```bash
    python src/legal_brief_companion/ingest.py
    ```

6.  Run the application:

    ```bash
    streamlit run app.py
    ```

### Uploads, OCR, and saved chats

- Upload one PDF or TXT file in the app (up to 50 MB). The app indexes it for the current session and uses its page text as the source for answers.
- Summary mode processes every extracted section in bounded batches, then combines the partial summaries with source page references. Question and argument modes continue to retrieve only the most relevant sections.
- Scanned PDF pages are read with PyMuPDF OCR. Install the Tesseract OCR engine and English language data on the machine running Streamlit; digital PDFs do not need Tesseract.
- Uploads are retained only for the active session unless **Remember this document and chat after refresh** is selected. When selected, the document and transcript are stored under `data/saved_sessions/` on the app server until the user clears them. The URL contains access to that saved session. Enable this only on a trusted, private deployment; do not share the URL or use this on a shared server without authentication and a data-retention policy.
- Users can export the conversation and source page references as JSON.

On Debian/Ubuntu, install the OCR engine with `sudo apt install tesseract-ocr tesseract-ocr-eng`. PyMuPDF is installed from the Python dependencies; Tesseract is a separate system package.

## 🧑‍⚖️ Usage

After running the application, you can interact with the assistant through the command-line interface or the Streamlit interface. Provide your queries, and the assistant will respond based on the ingested documents.

## 🧩 Components

- **Document Ingestion:** Load and chunk legal PDFs or text files using `document_loader.py` and `text_splitter.py`.
- **Vector Store Retrieval:** Embed and retrieve relevant chunks using ChromaDB, managed by `vector_store.py` and `retriever.py`.
- **LLM Interaction:** Generate answers using Groq-hosted LLaMA models, orchestrated by `chain.py`.
- **Prompt Templates:** Modular prompts for transparent reasoning, defined in `prompt_templates.py`.
- **User Interface:** Streamlit frontend (`app.py`) and CLI (`cli.py`) for flexible interaction.
- **Config Management:** Pydantic-based `.env` loader for reproducibility via `settings.py`.

## 🧩 Core Components

### Document Processing

- PDF and text file ingestion
- Intelligent document chunking
- Semantic embedding generation

### Retrieval System

- ChromaDB vector store integration
- Similarity-based chunk retrieval
- Context ranking and selection

### LLM Integration

- Groq-hosted LLaMA models
- Structured prompt engineering
- Response chain orchestration

## 🧪 Testing

Unit tests are included under `src/legal_brief_companion/tests/`. Run with:

```bash
PYTHONPATH=src pytest -q src/legal_brief_companion/tests/
```

## 🛠️ Built With

- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.chroma.com/)
- [Groq](https://www.groq.com/)
- [Streamlit](https://streamlit.io/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)

## 🔒 Security Notes

- Never commit your `.env` file or API keys to GitHub. The `.gitignore` file is set up to exclude secrets and unnecessary files.
- Use environment variables for secrets
- Follow security best practices
- Regular dependency updates

## 🔒 License

This project is licensed under the MIT License.

## 📬 Contact

Built by [Getahune Wondemenhu Alemayhu](https://www.github.com/getishe).

- Email: [getahune.alemayhu@gmail.com]
  For questions, contributions, or collaboration, feel free to reach out or open an issue.

## Contributions are welcome!

Please open issues or submit pull requests for improvements or bug fixes. Follow the existing code style and include tests for new features and suggestions.
