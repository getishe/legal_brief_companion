# RAG-Powered Assistant - Legal Brief Companion

This project implements a modular Retrieval-Augmented Generation (RAG) assistant using LangChain, designed to answer legal and technical queries based on custom documents. It features document ingestion, semantic retrieval, prompt templating, and LLM-backed response generation—all wrapped in a clean CLI and Streamlit interface.

## Project Structure

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
│       └── ingest.py                 # CLI/script entry for ingestion
├── data/
│   ├── documents/                    # User documents (PDFs, txt)
│   └── vector_store/                 # Persisted vector DB files
│       └── <instance-id>/
├── tests/
│   ├── test_ingestion.py
│   └── test_llm.py
├── app.py                            # Streamlit / main app entry
├── pyproject.toml
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

⚙️ Setup Instructions

1. Clone the repository:

```

git clone <repository-url>
cd legal_brief_companion

```

2. Install the required dependencies:

```

pip install -r requirements.txt

```

3. Set up your environment variables in the `.env` file.

```

GROQ_API_KEY=your_groq_key
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
DATABASE_URL=sqlite:///data/knowledge_base.db
DOCUMENTS_PATH=data/documents
PERSIST_DIRECTORY=data/vector_store
MODEL_NAME=llama3-8b-8192
VECTOR_STORE_TYPE=chroma

debug = true

```

4. Ingest your documents:

```

python run python src/legal_brief_companion/ingest.py

```

5. Ensure the vector store is created in the `data/vector_store` directory.

6. set your Groq Api key in the .env file

```

GROQ_API_KEY=your_api_key_here #power shell

export GROQ_API_KEY=your_api_key_here #linux/mac

```

7. Run the application:

```

python run streamlit run app.py

```

🧑‍⚖️ Usage

After running the application, you can interact with the assistant through the command-line interface. Provide your queries, and the assistant will respond based on the ingested documents.

🧩 Components

- Document Ingestion: Load and chunk legal PDFs or text files.

- Vector Store Retrieval: Embed and retrieve relevant chunks using ChromaDB.

- LLM Interaction: Generate answers using Groq-hosted LLaMA models.

- Prompt Templates: Modular prompts for teachable, transparent reasoning.

- User Interface: Streamlit frontend and CLI for flexible interaction.

- Config Management: Pydantic-based .env loader for reproducibility.

🧪 Testing

Basic unit tests are included under src/legal_brief_companion/tests/. Run with:

pytest src/legal_brief_companion/tests/

🛠️ Built With

[LangChain](https://www.langchain.com/)

[ChromaDB](https://www.chroma.com/)

[Groq](https://www.groq.com/)

[Streamlit](https://streamlit.io/)

[Pydantic](https://pydantic-docs.helpmanual.io/)

🔒 Security Notes

Never commit your .env or API keys to GitHub.
.gitignore is set up to exclude secrets and unnecessary files.

🔒 License

This project is licensed under the MIT License.

📬 Contact
Built by [Getahune Wondemenhu Alemayhu](https://www.github.com/getishe).

For questions, contributions, or collaboration, feel free to reach out or open an issue.

## Contributions are welcome!

Please open issues or submit pull requests for improvements or bug and follow the existing code style and include tests for new features.
