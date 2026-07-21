"""Monta o payload de conversação no formato role/content — é literalmente
o que qualquer API de chat (OpenAI, Anthropic, etc.) espera receber.

Aula 2.1 do curso: "O que existe por trás de um chat". Nenhuma LLM é chamada
aqui — só expomos a estrutura que uma geração real usaria. A Aula 2.8
introduz a fronteira generativa por meio de um componente local didático
(ver `chat.generative`/`chat.local_generation`); uma integração com LLM real
permanece fora desta etapa. Aula 2.3: a mensagem system passa a vir da
persona explícita (app/chat/persona.py), não de uma frase solta.
"""
from __future__ import annotations

from .persona import CUSTOMER_SUPPORT_PERSONA, build_system_prompt
from .state import Session
from .summary import render_summary

SYSTEM_PROMPT = build_system_prompt(CUSTOMER_SUPPORT_PERSONA)

RECENT_MESSAGE_LIMIT = 4
"""Limite PEDAGÓGICO e determinístico de mensagens recentes enviadas cruas no
payload (Aula 2.5) — quatro mensagens correspondem a duas rodadas completas.
Não corresponde à janela real de nenhum modelo específico. Histórico mais
antigo é compactado no resumo estruturado (`session.summary`, ver
`chat.summary`) — o histórico bruto (`session.messages`) nunca é apagado."""


def build_system_context(session: Session) -> str:
    """System prompt + resumo estruturado, só quando o histórico já passou de
    RECENT_MESSAGE_LIMIT — antes disso, o comportamento é idêntico ao das
    Aulas 2.1/2.3 (só a persona)."""
    if len(session.messages) <= RECENT_MESSAGE_LIMIT:
        return SYSTEM_PROMPT

    summary = render_summary(session.summary)
    return f"{SYSTEM_PROMPT}\n\nCONTEXTO RESUMIDO DA SESSÃO\n{summary}"


def build_payload(session: Session) -> list[dict[str, str]]:
    """Converte o estado da sessão numa lista ordenada de mensagens
    {"role", "content"} — sempre começando pelo system prompt (persona +
    resumo, quando houver compactação). Quando o histórico passa de
    RECENT_MESSAGE_LIMIT, só as mensagens mais recentes entram cruas no
    payload; `session.messages` continua com o histórico completo."""
    compacted = len(session.messages) > RECENT_MESSAGE_LIMIT
    messages = session.messages[-RECENT_MESSAGE_LIMIT:] if compacted else session.messages

    payload = [{"role": "system", "content": build_system_context(session)}]
    payload.extend({"role": m.role, "content": m.content} for m in messages)
    return payload
