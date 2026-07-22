"""Entry point do laboratório: FastAPI servindo a página estática + o fluxo de chat.

Aula 2.8: o componente generativo é construído uma única vez no boot, a
partir de `GENERATION_MODE` — nenhuma chamada de LLM, API externa ou serviço
pago acontecia; `local_didactic` era a única implementação real disponível
(ver `chat.local_generation.LocalDidacticComponent`).

Aula 3.8: `GENERATION_MODE=ollama` constrói `OllamaGenerativeComponent` (ver
`chat.ollama_generation`) — primeira inferência REAL do laboratório, via
Ollama local. Sem health-check no boot: o app sobe mesmo com o Ollama
desligado; a primeira falha real de chamada é que aciona o fallback.
"""
from __future__ import annotations

import os
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .chat.flow import handle_input
from .chat.generative import GenerativeComponent
from .chat.local_generation import LocalDidacticComponent
from .chat.ollama_generation import OllamaGenerativeComponent
from .chat.payload import build_payload
from .chat.state import Session

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="Customer Support Lab")

_sessions: dict[str, Session] = {}


def build_generative_component() -> GenerativeComponent | None:
    mode = os.getenv("GENERATION_MODE", "local_didactic").strip().lower()
    if mode == "local_didactic":
        return LocalDidacticComponent()
    if mode == "disabled":
        return None
    if mode == "ollama":
        return OllamaGenerativeComponent(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434"),
            model=os.getenv("OLLAMA_MODEL", "llama3.2:1b"),
            timeout_seconds=float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60")),
            num_ctx=int(os.getenv("OLLAMA_NUM_CTX", "2048")),
        )
    raise RuntimeError(f"GENERATION_MODE não suportado: {mode}")


_generative_component = build_generative_component()


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
    reply = handle_input(session, req.message, component=_generative_component)
    return ChatResponse(session_id=session_id, reply=reply)


@app.get("/api/chat/{session_id}/payload", response_model=PayloadResponse)
def chat_payload(session_id: str) -> PayloadResponse:
    """Aula 2.1: expõe o payload de conversação (role/content) que uma API de
    LLM receberia — nenhuma é chamada; a Aula 2.8 resolve texto livre com um
    componente local didático (ver `chat.local_generation`)."""
    session = _sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session_id não encontrado")
    return PayloadResponse(session_id=session_id, payload=build_payload(session))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
