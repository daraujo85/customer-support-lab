"""Política de resumo incremental da conversa — Aula 2.5 do curso.

O problema: `Session.messages` guarda o histórico bruto completo, e mandar
tudo a cada rodada infla o payload sem limite (Aula 2.4 já explicou o
porquê). A solução aqui NÃO chama nenhuma IA — a primeira chamada generativa
continua reservada pra Aula 2.8. O resumo é um retrato ESTRUTURADO e
determinístico (fatos, decisões, pendências, preferências), atualizado por
regra explícita de transição de estado — não uma cópia menor da transcrição.
"""
from __future__ import annotations

from .state import ChatState, ConversationSummary, Session

_PENDING_BY_STATE: dict[ChatState, str] = {
    ChatState.MAIN_MENU: "Escolher uma opção de atendimento.",
    ChatState.SUPORTE_TECNICO: "Descrever o problema técnico.",
    ChatState.FINANCEIRO: "Informar número do pedido ou fatura.",
    ChatState.INFORMACOES_CONTA: "Informar qual dado da conta precisa consultar.",
    ChatState.HUMAN_HANDOFF: "Aguardar atendimento humano.",
}

_LABEL_BY_STATE: dict[ChatState, str] = {
    ChatState.SUPORTE_TECNICO: "Suporte técnico",
    ChatState.FINANCEIRO: "Questões de faturamento",
    ChatState.INFORMACOES_CONTA: "Informações de conta",
    ChatState.HUMAN_HANDOFF: "Atendimento humano",
}

_ENCERRADO_DECISION = "Atendimento determinístico encerrado após coleta da informação."


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _set_pending(summary: ConversationSummary, value: str | None) -> None:
    summary.pending.clear()
    if value:
        summary.pending.append(value)


def update_summary(session: Session, previous_state: ChatState, user_input: str) -> None:
    """Atualiza `session.summary` a partir da transição que acabou de
    acontecer (`previous_state` -> `session.state`). Regras por transição:

    - GREETING -> MAIN_MENU: só cria a pendência de escolher uma opção (a
      mensagem vazia de abertura não vira fato).
    - MAIN_MENU -> MAIN_MENU (entrada inválida): nenhum fato/decisão novos.
    - MAIN_MENU -> <área>: registra a decisão de área selecionada + a
      pendência correspondente daquela área.
    - <área> -> ENCERRADO: registra o fato com a mensagem do usuário
      (formulação "Usuário informou..." — nunca afirma que o dado é válido)
      + a decisão de encerramento + limpa a pendência. Exceção: a partir de
      HUMAN_HANDOFF a pendência de aguardar atendimento humano permanece.
    - Mensagens depois de ENCERRADO: ignoradas (não alteram o resumo)."""
    summary = session.summary

    if previous_state == ChatState.GREETING and session.state == ChatState.MAIN_MENU:
        _set_pending(summary, _PENDING_BY_STATE[ChatState.MAIN_MENU])
        return

    if previous_state == ChatState.MAIN_MENU and session.state == ChatState.MAIN_MENU:
        return  # entrada inválida: nenhuma decisão/fato novo

    if previous_state == ChatState.MAIN_MENU and session.state in _LABEL_BY_STATE:
        _append_unique(
            summary.decisions,
            f"Área de atendimento selecionada: {_LABEL_BY_STATE[session.state]}.",
        )
        _set_pending(summary, _PENDING_BY_STATE[session.state])
        return

    if previous_state == ChatState.HUMAN_HANDOFF and session.state == ChatState.ENCERRADO:
        _append_unique(
            summary.facts,
            f"Usuário enviou informação adicional antes do atendimento humano: {user_input}.",
        )
        _set_pending(summary, _PENDING_BY_STATE[ChatState.HUMAN_HANDOFF])
        return

    if previous_state == ChatState.SUPORTE_TECNICO and session.state == ChatState.ENCERRADO:
        _append_unique(summary.facts, f"Usuário informou problema técnico: {user_input}.")
        _append_unique(summary.decisions, _ENCERRADO_DECISION)
        _set_pending(summary, None)
        return

    if previous_state == ChatState.FINANCEIRO and session.state == ChatState.ENCERRADO:
        _append_unique(summary.facts, f"Usuário informou referência de faturamento: {user_input}.")
        _append_unique(summary.decisions, _ENCERRADO_DECISION)
        _set_pending(summary, None)
        return

    if previous_state == ChatState.INFORMACOES_CONTA and session.state == ChatState.ENCERRADO:
        _append_unique(summary.facts, f"Usuário solicitou consulta de conta: {user_input}.")
        _append_unique(summary.decisions, _ENCERRADO_DECISION)
        _set_pending(summary, None)
        return

    # Mensagens depois de ENCERRADO (previous_state == ENCERRADO) ou qualquer
    # outra transição não mapeada: ignoradas — continuam só no histórico bruto.


def render_summary(summary: ConversationSummary) -> str:
    """Formato fixo com as quatro seções sempre presentes — deixa explícito
    que ausência de preferência não significa preferência inferida."""
    facts = "\n".join(f"- {f}" for f in summary.facts) or "- Nenhum fato registrado."
    decisions = "\n".join(f"- {d}" for d in summary.decisions) or "- Nenhuma decisão registrada."
    pending = "\n".join(f"- {p}" for p in summary.pending) or "- Nenhuma pendência registrada."
    preferences = (
        "\n".join(f"- {p}" for p in summary.preferences) or "- Nenhuma preferência explícita registrada."
    )
    return (
        "RESUMO DA CONVERSA\n\n"
        f"FATOS\n{facts}\n\n"
        f"DECISÕES\n{decisions}\n\n"
        f"PENDÊNCIAS\n{pending}\n\n"
        f"PREFERÊNCIAS\n{preferences}"
    )
