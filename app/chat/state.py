"""Estruturas do fluxo determinístico: estado, evento e transição.

Aula 1.3 do curso — máquina de estados finita, sem geração de linguagem.
Nada aqui conhece IA; a Aula 2.8 é quem introduz a primeira camada generativa.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


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
class Session:
    """Estado de uma conversa. Nada é persistido nesta aula (Aula 2.6 introduz
    a separação entre estado de usuário, de sessão e de execução)."""

    state: ChatState = ChatState.GREETING
    history: list[str] = field(default_factory=list)
