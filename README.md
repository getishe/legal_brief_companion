# rag-assistant/README.md

# RAG-Powered Assistant

This project implements a simple RAG (Retrieval-Augmented Generation) powered assistant using LangChain. The assistant answers questions based on a custom document set and includes various components for prompt formulation, vector store retrieval, LLM-generated responses, document ingestion, and a basic user interface for interaction.

## Project Structure

```
rag-assistant
├── src
│   ├── app.py                  # Main entry point of the application
│   ├── config
│   │   └── settings.py         # Configuration settings for the application
│   ├── ingestion
│   │   ├── document_loader.py   # Handles loading documents into the application
│   │   └── text_splitter.py     # Splits large documents into smaller chunks
│   ├── retrieval
│   │   ├── vector_store.py      # Manages storage and retrieval of document embeddings
│   │   └── retriever.py         # Fetches relevant documents based on user queries
│   ├── llm
│   │   ├── chain.py             # Orchestrates interaction with the language model
│   │   └── prompt_templates.py   # Provides formatted prompt templates
│   ├── interface
│   │   └── cli.py               # Command-line interface for user interaction
│   └── utils
│       └── helpers.py           # Utility functions for various tasks
├── data
│   └── documents                # Directory for storing custom documents
├── requirements.txt             # Python dependencies for the project
├── .env                         # Environment variables for configuration
└── README.md                    # Documentation for the project

```

## Setup Instructions

1. Clone the repository:

   ```
   git clone <repository-url>
   cd rag-assistant
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in the `.env` file.

4. Run the application:
   ```
   python src/app.py
   ```

## Usage

After running the application, you can interact with the assistant through the command-line interface. Provide your queries, and the assistant will respond based on the ingested documents.

## Components

- **Document Ingestion**: Load and preprocess documents for the assistant.
- **Vector Store Retrieval**: Efficiently retrieve relevant documents using embeddings.
- **LLM Interaction**: Generate responses using a language model.
- **User Interface**: Simple CLI for user interaction.

Feel free to explore the code and modify it to suit your needs!

"& { $(irm https://aka.ms/install-powershell.ps1) } -UseMSI"

power shell

https://copilot.microsoft.com/shares/QERQyvTyiG3sZ654RACGW

https://copilot.microsoft.com/shares/W2VehnXKzxn4urnFdubQC

https://copilot.microsoft.com/shares/FPkRs3BoRB895WGwCFAKn

https://copilot.microsoft.com/shares/A3xiSVePWTzHHoddNLRbU

Project
https://copilot.microsoft.com/shares/hqmWtuCsx6v4MrtBEYuNR
https://copilot.microsoft.com/chats/DcSDLVGWo5TV6B8uRziR4
https://pwskills.com/blog/how-to-develop-an-effective-ai-legal-assistant/

https://copilot.microsoft.com/chats/REFhrMCUgFWzyxo5kPf7y

https://copilot.microsoft.com/chats/bdEHjKkpzhKQ4oZyD4QgQ

https://copilot.microsoft.com/chats/DcSDLVGWo5TV6B8uRziR4

<!-- EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
LLM_PROVIDER=groq
LLM_MODEL=llama-3.1-8b-instant
DATABASE_URL=sqlite:///data/knowledge_base.db
DOCUMENTS_PATH=data/documents
PERSIST_DIRECTORY=data/vector_store -->
 <!-- poetry run python src/legal_brief_companion/ingest.py -->
<!-- poetry run streamlit run src/legal_brief_companion/app.py -->
<!-- https://github.com/Dnyaneshwar-dnyanu/Weather-App -->
