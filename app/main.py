"""Entry point do laboratório: FastAPI servindo a página estática + o fluxo de chat.

Aula 1.3: só o determinístico. Nenhuma chamada de LLM existe neste arquivo ainda.
"""
from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .chat.flow import handle_input
from .chat.payload import build_payload
from .chat.state import Session

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Customer Support Lab")

_sessions: dict[str, Session] = {}


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str = ""


class ChatResponse(BaseModel):
    session_id: str
    reply: str


class PayloadResponse(BaseModel):
    session_id: str
    payload: list[dict[str, str]]


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id or str(uuid4())
    session = _sessions.setdefault(session_id, Session())
    reply = handle_input(session, req.message)
    return ChatResponse(session_id=session_id, reply=reply)


@app.get("/api/chat/{session_id}/payload", response_model=PayloadResponse)
def chat_payload(session_id: str) -> PayloadResponse:
    """Aula 2.1: expõe o payload de conversação (role/content) que uma API de
    LLM receberia — ainda sem chamar nenhuma (isso é a Aula 2.8)."""
    session = _sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session_id não encontrado")
    return PayloadResponse(session_id=session_id, payload=build_payload(session))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
