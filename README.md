# Legal Brief Companion

Legal Brief Companion lets a user upload one case-related PDF or text document and chat with its contents. The Streamlit app extracts and indexes the document, answers questions from relevant passages, and can summarize the full document with page references.

The app provides legal research assistance only. Verify the source document, citations, and conclusions with a qualified attorney.

**Live app:** [legalbriefcompanion.streamlit.app](https://legalbriefcompanion.streamlit.app/)

## Requirements

- Python 3.11 or newer
- A Groq API key
- Tesseract OCR with English language data for scanned PDFs

## Install and run

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   If you use Poetry, regenerate the lockfile after adding dependencies with `poetry lock`, then install with `poetry install`.

2. Set the Groq API key in your environment:

   **Linux/macOS**

   ```bash
   export GROQ_API_KEY="your_groq_api_key"
   ```

   **PowerShell**

   ```powershell
   $env:GROQ_API_KEY="your_groq_api_key"
   ```

   Optional settings include:

   ```env
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   LLM_MODEL=openai/gpt-oss-20b
   PERSIST_DIRECTORY=data/vector_store
   DOCUMENTS_PATH=data/documents
   ```

3. Start the app:

   ```bash
   streamlit run app.py
   ```

4. Upload one PDF or TXT file, select **Index document**, then ask questions in the chat.

The app offers `openai/gpt-oss-20b` and `openai/gpt-oss-120b` through Groq. The response-length control is an output ceiling, with a 1,024-token default; increase it for longer answers. The app prompts for concise, source-grounded responses.

## Document handling

- A single PDF or TXT file up to 50 MB can be uploaded at a time. A new indexed upload replaces the active document and clears its chat.
- PDF citations use one-based page numbers. Text files have no page numbers, so their source trail identifies the file.
- Question, argument, and citation modes retrieve the four most relevant sections.
- **Summary** mode processes every extracted section in bounded batches, then combines the results. It describes the type of document it actually receives instead of assuming every upload is a court opinion. Progress is shown during summarization.
- Scanned PDF pages with no extractable text are processed with PyMuPDF OCR. PyMuPDF is a Python dependency; Tesseract is a separate system package. On Debian/Ubuntu, install it with:

  ```bash
  sudo apt install tesseract-ocr tesseract-ocr-eng
  ```

  OCR currently uses English. Digital PDFs do not require Tesseract.

## Chat export and saved sessions

Use **Export chat with citations (JSON)** to download the conversation and source passages/page references.

By default, uploads are kept for the active Streamlit session and are not added to the shared vector store. The optional **Remember this document and chat after refresh** setting stores the original upload and chat under `data/saved_sessions/` on the app server. The page URL grants access to that saved session. Enable this only on a trusted, private deployment, do not share the URL, and use **Clear current document and chat** to remove the saved files. The saved-session directory is excluded from Git.

## Existing command-line ingestion

The repository also includes a CLI for indexing files from `DOCUMENTS_PATH` into the persistent Chroma store:

```bash
PYTHONPATH=src python src/interface/cli.py ingest
PYTHONPATH=src python src/interface/cli.py query "What does the document say about the issue?"
```

The Streamlit upload flow does not require CLI ingestion.

## Project layout

```text
app.py                                  Streamlit upload and chat interface
src/ingestion/                          Document loading and text splitting
src/interface/cli.py                    CLI ingestion and query commands
src/legal_brief_companion/config/       Settings and logging
src/legal_brief_companion/llm/          Retrieval chain, whole-document summary, prompts
src/legal_brief_companion/retrieval/    Chroma vector-store helpers
src/legal_brief_companion/session_store.py  Opt-in local session persistence
src/legal_brief_companion/tests/        Unit tests
data/documents/                         Optional CLI source documents
data/vector_store/                      Persistent CLI vector store
data/saved_sessions/                    Opt-in saved uploads and chats (Git-ignored)
```

## Tests

```bash
PYTHONPATH=src pytest -q src/legal_brief_companion/tests/
```

## Security and privacy

- Keep API keys out of source control. The `.env` file is Git-ignored; environment variables are recommended for secrets.
- Uploaded documents are sent to the configured Groq service as context for generation. Review the provider’s data handling terms before uploading sensitive case files.
- Saved sessions are stored on the machine running the app. Do not enable persistence on a shared or public deployment without authentication, access controls, and a retention policy.
- Generated answers may be incomplete or incorrect. Confirm legal authorities and page citations against the original document.

## License

MIT. See [LICENSE](LICENSE).
