"""Contrato do componente generativo — Aula 2.8 do curso.

Esta aula introduz a FRONTEIRA generativa da arquitetura, não uma inferência
real: nenhuma chamada de LLM, API externa, modelo local ou serviço pago
acontece neste laboratório. A implementação usada em runtime
(`LocalDidacticComponent`, ver `chat.local_generation`) é um componente local,
determinístico e didático que simula o CONTRATO de uma integração
probabilística — classificação de intenção, score de confiança e geração de
resposta — sem aleatoriedade e sempre reproduzível.

O contrato (`GenerativeComponent`) é o que permite, no futuro, substituir essa
implementação local por um provider real (API paga, modelo local, etc.) sem
reescrever a máquina de estados, o resumo ou os testes de domínio.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal, Protocol


class Intent(str, Enum):
    SUPORTE_TECNICO = "suporte_tecnico"
    FINANCEIRO = "financeiro"
    INFORMACOES_CONTA = "informacoes_conta"
    HUMAN_HANDOFF = "human_handoff"
    UNKNOWN = "unknown"


class ResolutionMode(str, Enum):
    """Como um turno foi resolvido — registrado no resumo estruturado
    (`chat.summary`) pra deixar explícito quando a resposta veio de regra
    determinística pura, do componente local didático ou de fallback."""

    DETERMINISTIC = "deterministic"
    LOCAL_DIDACTIC = "local_didactic"
    FALLBACK = "fallback"


MIN_ACCEPTED_SCORE = 0.70
"""Limite mínimo de score pra aceitar uma classificação — abaixo disso, o
fluxo trata como UNKNOWN e aciona o fallback determinístico."""


@dataclass(frozen=True)
class GeneratedTurn:
    """Resultado do componente generativo pra um turno de texto livre.

    `score` é um número entre 0 e 1 calculado por regras locais — NÃO
    representa uma probabilidade calibrada de nenhum modelo estatístico."""

    intent: Intent
    score: float
    reply: str
    matched_terms: tuple[str, ...]
    source: Literal["local_didactic"] = "local_didactic"


MessagePayload = list[dict[str, str]]


class GenerativeComponentError(RuntimeError):
    """Erro do componente generativo — o fluxo trata como fallback determinístico."""


class GenerativeComponent(Protocol):
    """Contrato substituível: o `flow.py` não precisa saber se a implementação
    é regras locais, uma API remota, um modelo local ou um double de teste."""

    def generate(
        self,
        *,
        messages: MessagePayload,
        user_input: str,
        expected_intent: Intent | None = None,
    ) -> GeneratedTurn: ...


def build_generative_messages(session, user_input: str) -> MessagePayload:
    """Contexto que um provider real receberia: o payload já construído
    (persona + resumo + mensagens recentes, ver `chat.payload.build_payload`)
    mais a mensagem atual do usuário. Preserva a arquitetura das aulas
    anteriores — o componente local pode ignorar parte desse contexto
    internamente, mas o contrato já é o mesmo que uma integração real usaria."""
    from .payload import build_payload

    messages = build_payload(session)
    messages.append({"role": "user", "content": user_input})
    return messages
