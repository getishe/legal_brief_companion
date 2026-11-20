import hashlib
import json
import os
import sys
import tempfile
import uuid
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

from ingestion.text_splitter import split_documents
from legal_brief_companion.config.settings import settings
from legal_brief_companion.llm.chain import build_chain, summarize_documents
from legal_brief_companion.retrieval.vector_store import build_upload_vector_store
from legal_brief_companion.session_store import delete_session, load_session, save_session


MAX_UPLOAD_MB = 50


def _load_uploaded_document(name, content, progress_callback=None):
    """Extract one PDF/TXT and attach stable source and page citation metadata."""
    suffix = Path(name).suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise ValueError("Upload a PDF or TXT document.")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        loader = PyPDFLoader(temp_path) if suffix == ".pdf" else TextLoader(
            temp_path, encoding="utf-8"
        )
        documents = loader.load()

        ocr_pages = 0
        ocr_warnings = []
        if suffix == ".pdf":
            blank_pages = [
                doc for doc in documents if not doc.page_content.strip()
            ]
            if blank_pages:
                try:
                    import pymupdf
                except ImportError as exc:
                    raise RuntimeError(
                        "This PDF has scanned pages. Install the PyMuPDF dependency "
                        "and the Tesseract OCR engine to read them."
                    ) from exc

                pdf = pymupdf.open(temp_path)
                try:
                    for index, doc in enumerate(blank_pages, 1):
                        page_number = doc.metadata.get("page", 0)
                        if progress_callback:
                            progress_callback(
                                0.2 + 0.45 * index / len(blank_pages),
                                f"Running OCR on scanned page {page_number + 1}...",
                            )
                        try:
                            page = pdf[page_number]
                            text_page = page.get_textpage_ocr(
                                language="eng", dpi=200, full=True
                            )
                            extracted = page.get_text(textpage=text_page).strip()
                            if extracted:
                                doc.page_content = extracted
                                doc.metadata["ocr"] = True
                                ocr_pages += 1
                            else:
                                ocr_warnings.append(page_number + 1)
                        except Exception:
                            ocr_warnings.append(page_number + 1)
                finally:
                    pdf.close()

        for doc in documents:
            zero_based_page = doc.metadata.get("page")
            doc.metadata["source"] = Path(name).name
            doc.metadata["page"] = (
                zero_based_page + 1 if isinstance(zero_based_page, int) else "N/A"
            )

        documents = [doc for doc in documents if doc.page_content.strip()]
        if not documents:
            raise ValueError(
                "No readable text was found. For scanned PDFs, install Tesseract "
                "with the English language data and try again."
            )
        return documents, ocr_pages, ocr_warnings
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


def _restore_saved_session(session_id):
    """Load an explicitly saved upload and rebuild its transient vector index."""
    saved = load_session(session_id)
    if not saved:
        return False
    documents, _, _ = _load_uploaded_document(
        saved["document_name"], saved["document_bytes"]
    )
    chunks = split_documents(documents)
    st.session_state.upload_vector_store = build_upload_vector_store(chunks)
    st.session_state.uploaded_chunks = chunks
    st.session_state.uploaded_pages = documents
    st.session_state.active_document_name = saved["document_name"]
    st.session_state.active_document_bytes = saved["document_bytes"]
    st.session_state.active_upload_hash = hashlib.sha256(
        saved["document_bytes"]
    ).hexdigest()
    st.session_state.chat_messages = [
        {
            **message,
            "sources": [
                Document(
                    page_content=source["page_content"],
                    metadata=source.get("metadata", {}),
                )
                for source in message.get("sources", [])
            ],
        }
        for message in saved["messages"]
    ]
    st.session_state.remember_upload = True
    st.session_state.saved_session_id = session_id
    return True


def _save_current_session():
    session_id = st.session_state.get("saved_session_id") or str(uuid.uuid4())
    save_session(
        session_id,
        st.session_state.active_document_name,
        st.session_state.active_document_bytes,
        st.session_state.chat_messages,
    )
    st.session_state.saved_session_id = session_id
    st.query_params["saved_session"] = session_id


def main():
    st.set_page_config(page_title="Legal Brief Companion", layout="wide")
    st.title("⚖️ Legal Brief Companion")
    st.caption(
        "Chat with one case document at a time. Answers use the uploaded document "
        "and include source page references. Verify legal conclusions with a qualified attorney."
    )

    try:
        for secret_name in ("GROQ_API_KEY", "EMBEDDING_MODEL", "LLM_MODEL"):
            if secret_name not in os.environ:
                secret_value = st.secrets.get(secret_name)
                if secret_value:
                    os.environ[secret_name] = str(secret_value)
    except Exception:
        pass
    for setting_name in ("GROQ_API_KEY", "EMBEDDING_MODEL", "LLM_MODEL"):
        if os.environ.get(setting_name):
            setattr(settings, setting_name, os.environ[setting_name])

    st.session_state.setdefault("active_upload_hash", None)
    st.session_state.setdefault("active_document_name", None)
    st.session_state.setdefault("active_document_bytes", None)
    st.session_state.setdefault("uploaded_chunks", [])
    st.session_state.setdefault("uploaded_pages", [])
    st.session_state.setdefault("upload_vector_store", None)
    st.session_state.setdefault("chat_messages", [])
    st.session_state.setdefault("remember_upload", False)
    st.session_state.setdefault("saved_session_id", None)

    saved_session_id = st.query_params.get("saved_session")
    if saved_session_id and st.session_state.upload_vector_store is None:
        try:
            with st.spinner("Restoring your saved document and chat..."):
                restored = _restore_saved_session(saved_session_id)
            if not restored:
                st.warning("The saved session could not be found. Upload the document again.")
        except Exception as exc:
            st.error(f"Could not restore the saved session: {exc}")

    api_key_configured = settings.GROQ_API_KEY not in ("demo-key", None, "")
    if not api_key_configured:
        st.warning("Set GROQ_API_KEY in your environment or Streamlit secrets to ask questions.")

    uploaded_file = st.file_uploader(
        "Upload the case document you want to chat with",
        type=["pdf", "txt"],
        help=f"PDF or TXT, up to {MAX_UPLOAD_MB} MB. Uploads stay in session memory unless you opt into server-side saving below.",
    )
    if uploaded_file is not None:
        st.caption(f"Selected: {uploaded_file.name} · {uploaded_file.size / (1024 * 1024):.1f} MB")
        if uploaded_file.size > MAX_UPLOAD_MB * 1024 * 1024:
            st.error(f"This file exceeds the {MAX_UPLOAD_MB} MB upload limit.")
            return

    remember_default = bool(st.session_state.remember_upload)
    remember_upload = st.checkbox(
        "Remember this document and chat after refresh",
        value=remember_default,
        help="If enabled, the uploaded file and chat are stored on this app's server until you clear them. The page URL contains access to this saved session, so use only on a trusted, private deployment and do not share the URL.",
    )
    if remember_upload != st.session_state.remember_upload:
        st.session_state.remember_upload = remember_upload
        if not remember_upload and st.session_state.saved_session_id:
            delete_session(st.session_state.saved_session_id)
            st.session_state.saved_session_id = None
            st.query_params.pop("saved_session", None)
        elif (
            remember_upload
            and st.session_state.upload_vector_store is not None
            and st.session_state.active_document_bytes
        ):
            _save_current_session()

    if st.session_state.upload_vector_store is not None:
        if st.button("Clear current document and chat"):
            if st.session_state.saved_session_id:
                delete_session(st.session_state.saved_session_id)
            st.query_params.pop("saved_session", None)
            for key, value in {
                "upload_vector_store": None,
                "active_upload_hash": None,
                "active_document_name": None,
                "active_document_bytes": None,
                "uploaded_chunks": [],
                "uploaded_pages": [],
                "chat_messages": [],
                "saved_session_id": None,
                "remember_upload": False,
            }.items():
                st.session_state[key] = value
            st.rerun()

    model = st.selectbox("Model", ["openai/gpt-oss-20b", "openai/gpt-oss-120b"])
    query_type = st.selectbox("Response style", ["question", "summary", "argument", "citation"])
    response_tokens = st.slider(
        "Maximum response length (tokens)",
        min_value=512,
        max_value=4096,
        value=1024,
        step=256,
        help="This is an output ceiling. The prompt asks for concise answers; increase it only when you need more detail or longer tables.",
    )
    show_resources = st.checkbox("Show retrieved passages and page references")

    upload_hash = None
    upload_bytes = None
    if uploaded_file is not None:
        upload_bytes = uploaded_file.getvalue()
        upload_hash = hashlib.sha256(upload_bytes).hexdigest()
        if st.button("Index document", type="primary"):
            progress = st.progress(0, text="Starting document processing...")
            status = st.empty()
            try:
                documents, ocr_pages, ocr_warnings = _load_uploaded_document(
                    uploaded_file.name,
                    upload_bytes,
                    progress_callback=lambda value, message: (
                        progress.progress(min(value, 0.7), text=message)
                    ),
                )
                progress.progress(0.72, text="Splitting into searchable sections...")
                chunks = split_documents(documents)
                progress.progress(0.78, text="Creating a private session index...")
                vector_store = build_upload_vector_store(chunks)
                progress.progress(1.0, text="Indexing complete")
                st.session_state.upload_vector_store = vector_store
                st.session_state.uploaded_chunks = chunks
                st.session_state.uploaded_pages = documents
                st.session_state.active_upload_hash = upload_hash
                st.session_state.active_document_name = Path(uploaded_file.name).name
                st.session_state.active_document_bytes = upload_bytes
                st.session_state.chat_messages = []
                status.success(
                    f"Indexed {len(chunks)} searchable sections from {len(documents)} pages/sections."
                )
                if ocr_pages:
                    st.info(f"OCR extracted text from {ocr_pages} scanned page(s).")
                if ocr_warnings:
                    st.warning(
                        "OCR could not read page(s): "
                        + ", ".join(map(str, ocr_warnings))
                    )
                if remember_upload:
                    _save_current_session()
                st.rerun()
            except Exception as exc:
                status.error(f"Could not index this document ({type(exc).__name__}): {exc}")

        if st.session_state.active_upload_hash != upload_hash:
            st.info("Index this upload to start chatting. A different document will replace the current session.")
            return

    if st.session_state.upload_vector_store is None:
        st.info("Upload a PDF or text file, then index it to begin.")
        return

    st.markdown(f"**Current document:** {st.session_state.active_document_name}")
    if remember_upload:
        st.caption(
            "This document and chat are saved on the app server until cleared. "
            "The URL grants access to this saved session; do not share it."
        )
    settings.LLM_MODEL = model

    export_data = {
        "document": st.session_state.active_document_name,
        "messages": [
            {
                "role": message["role"],
                "content": message["content"],
                "sources": [
                    {
                        "source": doc.metadata.get("source"),
                        "page": doc.metadata.get("page"),
                        "text": doc.page_content,
                    }
                    for doc in message.get("sources", [])
                ],
            }
            for message in st.session_state.chat_messages
        ],
    }
    st.download_button(
        "Export chat with citations (JSON)",
        data=json.dumps(export_data, ensure_ascii=False, indent=2),
        file_name="legal_brief_chat.json",
        mime="application/json",
    )

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if show_resources and message.get("sources"):
                with st.expander("Sources used"):
                    for index, doc in enumerate(message["sources"], 1):
                        st.markdown(
                            f"**{index}. {doc.metadata.get('source', 'Unknown')} — "
                            f"page {doc.metadata.get('page', 'N/A')}**"
                        )
                        st.write(doc.page_content)

    prompt = st.chat_input(
        "Ask a question about this document",
        disabled=not api_key_configured,
    )
    if prompt:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        try:
            prior_messages = st.session_state.chat_messages[:-1][-6:]
            history = "\n".join(
                f"{item['role'].title()}: {item['content']}" for item in prior_messages
            )
            chain_question = (
                f"Conversation so far:\n{history}\n\nCurrent question: {prompt}"
                if history
                else prompt
            )
            with st.chat_message("assistant"):
                if query_type == "summary":
                    summary_progress = st.progress(
                        0, text="Preparing a full-document summary..."
                    )
                    answer = summarize_documents(
                        st.session_state.uploaded_chunks,
                        request=chain_question,
                        max_tokens=response_tokens,
                        progress_callback=lambda value, message: summary_progress.progress(
                            value, text=message
                        ),
                    )
                    sources = st.session_state.uploaded_pages
                else:
                    retriever = st.session_state.upload_vector_store.as_retriever(
                        search_kwargs={"k": 4}
                    )
                    chain = build_chain(
                        query_type,
                        max_chunks=4,
                        max_tokens=response_tokens,
                        retriever=retriever,
                    )
                    with st.spinner("Searching the document and drafting a sourced answer..."):
                        output = chain.invoke({"query": chain_question})
                    answer = output["result"]
                    sources = output.get("source_documents", [])
                st.markdown(answer)
                if show_resources and sources:
                    with st.expander("Sources used", expanded=True):
                        for index, doc in enumerate(sources, 1):
                            st.markdown(
                                f"**{index}. {doc.metadata.get('source', 'Unknown')} — "
                                f"page {doc.metadata.get('page', 'N/A')}**"
                            )
                            st.write(doc.page_content)
            st.session_state.chat_messages.append(
                {"role": "assistant", "content": answer, "sources": sources}
            )
            if remember_upload:
                _save_current_session()
        except Exception as exc:
            st.error(f"The response could not be generated ({type(exc).__name__}): {exc}")
            if settings.debug:
                st.exception(exc)


if __name__ == "__main__":
    main()
