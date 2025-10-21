# RAG-Powered Assistant - Legal Brief Companion

This project implements a modular Retrieval-Augmented Generation (RAG) assistant using LangChain, designed to answer legal and technical queries based on custom documents. It features document ingestion, semantic retrieval, prompt templating, and LLM-backed response generation—all wrapped in a clean CLI and Streamlit interface.

## Project Structure

legal_brief_companion/
├── src
│ ├── interface
│ │ └── cli.py # Command-line interface for user interaction
│ ├── ingestion
│ │ ├── document_loader.py # Handles loading documents into the application
│ │ └── text_splitter.py # Splits large documents into smaller chunks
│ ├── utils
| │ └── helpers.py
| legal_brief_companion
│ |
| ├── config
│ │ └── settings.py # Configuration settings for the application
│ ├── retrieval
│ │ ├── vector_store.py # Manages storage and retrieval of document embeddings
│ │ └── retriever.py # Fetches relevant documents based on user queries
│ ├── llm
│ │ ├── chain.py # Orchestrates interaction with the language model
│ | └── prompt_templates.py # Provides formatted prompt templates
│ |────tests
| | |
│ | |── test_ingestion.py
| | ├── test_llm.py
| |
│ |───────**init**.py # Orchestrates interaction with the language model
| |───────ingest.py
├── data
│ |── documents # Directory for storing custom documents
| | └──Tinker v. Des Moines (8th Cir.).pdf #Document pdf
| |
| |── vector_store
| | └── 06f38c0e-1645-4d2e-93af-207912a919dd
| | ├──data_level0.bin
│ | |──header.bin
| | ├──length.bin
│ | └──link_lists.bin
| └─────chroma.sqlite3
├── .gitignore
├── poetry.lock
├── pyproject.toml
|── app.py # Main entry point of the application
├── requirements.txt # Python dependencies for the project
├── .env # Environment variables for configuration
└── README.md # Documentation for the project

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


📬 Contact
Built by [Getahune Wondemenhu Alemayhu](https://www.github.com/getishe).
For questions, contributions, or collaboration, feel free to reach out or open an issue.

## Contributions are welcome!
  Please open issues or submit pull requests for improvements or bug fixes.
  Please follow the existing code style and include tests for new features.

```
