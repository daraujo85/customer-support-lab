"""Estruturas do fluxo determinístico: estado, evento e transição.

Aula 1.3 do curso — máquina de estados finita, sem geração de linguagem.
Nada aqui conhece IA; a Aula 2.8 introduz a fronteira generativa por meio de
um componente local didático — nenhuma chamada de LLM real acontece.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class ChatState(str, Enum):
    GREETING = "greeting"
    MAIN_MENU = "main_menu"
    SUPORTE_TECNICO = "suporte_tecnico"
    FINANCEIRO = "financeiro"
    INFORMACOES_CONTA = "informacoes_conta"
    HUMAN_HANDOFF = "human_handoff"
    ENCERRADO = "encerrado"


@dataclass
class MenuOption:
    key: str
    label: str
    next_state: ChatState


@dataclass
class Message:
    """Uma entrada da conversa no formato role/content que qualquer API de
    chat (OpenAI, Anthropic, etc.) espera receber. Aula 2.1 do curso."""

    role: Literal["system", "user", "assistant"]
    content: str


@dataclass
class ConversationSummary:
    """Retrato estruturado do que importa na conversa — Aula 2.5. Não é uma
    cópia menor da transcrição: cada campo tem uma responsabilidade própria,
    atualizada por regra determinística de transição (ver `chat.summary`),
    nunca por geração de linguagem (isso só chega na Aula 2.8)."""

    facts: list[str] = field(default_factory=list)
    decisions: list[str] = field(default_factory=list)
    pending: list[str] = field(default_factory=list)
    preferences: list[str] = field(default_factory=list)


@dataclass
class Session:
    """Estado de uma conversa. Nada é persistido nesta aula (Aula 2.6 introduz
    a separação entre estado de usuário, de sessão e de execução)."""

    state: ChatState = ChatState.GREETING
    messages: list[Message] = field(default_factory=list)
    summary: ConversationSummary = field(default_factory=ConversationSummary)
    """Resumo estruturado, atualizado incrementalmente a cada transição (ver
    `chat.summary.update_summary`) — `messages` continua guardando o
    histórico bruto completo; resumo e histórico bruto cumprem
    responsabilidades diferentes (ver `chat.payload.build_payload`)."""
