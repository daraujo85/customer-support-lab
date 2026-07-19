"""Entry point do laboratório: FastAPI servindo a página estática + o fluxo de chat.

Aula 1.3: só o determinístico. Nenhuma chamada de LLM existe neste arquivo ainda.
"""
from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .chat.flow import handle_input
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


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    session_id = req.session_id or str(uuid4())
    session = _sessions.setdefault(session_id, Session())
    reply = handle_input(session, req.message)
    return ChatResponse(session_id=session_id, reply=reply)


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
