"""Monta o payload de conversação no formato role/content — é literalmente
o que qualquer API de chat (OpenAI, Anthropic, etc.) espera receber.

Aula 2.1 do curso: "O que existe por trás de um chat". Nenhuma LLM é chamada
aqui — só expomos a estrutura que uma geração real usaria (isso chega na
Aula 2.8).
"""
from __future__ import annotations

from .state import Session

# Propositalmente genérico — a Aula 2.3 (Persona não é fantasia) é quem
# define identidade, escopo e comportamento de verdade. Não antecipar.
SYSTEM_PROMPT = "Você é o assistente de atendimento ao cliente."


def build_payload(session: Session) -> list[dict[str, str]]:
    """Converte o estado da sessão numa lista ordenada de mensagens
    {"role", "content"} — sempre começando pelo system prompt."""
    payload = [{"role": "system", "content": SYSTEM_PROMPT}]
    payload.extend({"role": m.role, "content": m.content} for m in session.messages)
    return payload
