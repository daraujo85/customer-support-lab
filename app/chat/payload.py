"""Monta o payload de conversação no formato role/content — é literalmente
o que qualquer API de chat (OpenAI, Anthropic, etc.) espera receber.

Aula 2.1 do curso: "O que existe por trás de um chat". Nenhuma LLM é chamada
aqui — só expomos a estrutura que uma geração real usaria (isso chega na
Aula 2.8). Aula 2.3: a mensagem system passa a vir da persona explícita
(app/chat/persona.py), não de uma frase solta.
"""
from __future__ import annotations

from .persona import CUSTOMER_SUPPORT_PERSONA, build_system_prompt
from .state import Session

SYSTEM_PROMPT = build_system_prompt(CUSTOMER_SUPPORT_PERSONA)


def build_payload(session: Session) -> list[dict[str, str]]:
    """Converte o estado da sessão numa lista ordenada de mensagens
    {"role", "content"} — sempre começando pelo system prompt."""
    payload = [{"role": "system", "content": SYSTEM_PROMPT}]
    payload.extend({"role": m.role, "content": m.content} for m in session.messages)
    return payload
