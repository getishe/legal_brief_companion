"""Opt-in local persistence for uploaded case documents and chat history."""

import json
import os
import uuid
from pathlib import Path

from legal_brief_companion.config.settings import settings


SESSION_ROOT = settings.PERSIST_DIR.parent / "saved_sessions"


def _session_dir(session_id: str) -> Path:
    # Accept only UUIDs so query parameters cannot become filesystem paths.
    safe_id = str(uuid.UUID(session_id))
    return SESSION_ROOT / safe_id


def save_session(session_id: str, document_name: str, document_bytes: bytes, messages: list):
    session_dir = _session_dir(session_id)
    session_dir.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(session_dir, 0o700)
    except OSError:
        pass
    suffix = Path(document_name).suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        raise ValueError("Only PDF and TXT uploads can be saved.")

    document_path = session_dir / f"document{suffix}"
    document_path.write_bytes(document_bytes)
    try:
        os.chmod(document_path, 0o600)
    except OSError:
        pass
    serializable_messages = []
    for message in messages:
        serializable_messages.append(
            {
                "role": message["role"],
                "content": message["content"],
                "sources": [
                    {
                        "page_content": doc.page_content,
                        "metadata": doc.metadata,
                    }
                    for doc in message.get("sources", [])
                ],
            }
        )
    metadata_path = session_dir / "session.json"
    metadata_path.write_text(
        json.dumps(
            {"document_name": Path(document_name).name, "messages": serializable_messages},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    try:
        os.chmod(metadata_path, 0o600)
    except OSError:
        pass


def load_session(session_id: str):
    session_dir = _session_dir(session_id)
    metadata_path = session_dir / "session.json"
    if not metadata_path.is_file():
        return None

    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    suffix = Path(data["document_name"]).suffix.lower()
    if suffix not in {".pdf", ".txt"}:
        return None
    document_path = session_dir / f"document{suffix}"
    if not document_path.is_file():
        return None
    return {
        "document_name": Path(data["document_name"]).name,
        "document_bytes": document_path.read_bytes(),
        "messages": data.get("messages", []),
    }


def delete_session(session_id: str):
    session_dir = _session_dir(session_id)
    for path in session_dir.iterdir() if session_dir.exists() else []:
        if path.is_file():
            path.unlink()
    if session_dir.exists():
        session_dir.rmdir()
