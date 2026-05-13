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
    LLM_MODEL=llama3-8b-8192
    DATABASE_URL=sqlite:///data/knowledge_base.db
    DOCUMENTS_PATH=data/documents
    PERSIST_DIRECTORY=data/vector_store
    MODEL_NAME=llama3-8b-8192
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

5.  Ingest your documents: This process will create the vector store.

    ```bash
    python src/legal_brief_companion/ingest.py
    ```

6.  Run the application:

    ```bash
    streamlit run app.py
    ```

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

Basic unit tests are included under `src/legal_brief_companion/tests/`. Run with:

```bash
pytest src/legal_brief_companion/tests/
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
