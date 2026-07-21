"""Política de resumo incremental da conversa — Aula 2.5 do curso.

O problema: `Session.messages` guarda o histórico bruto completo, e mandar
tudo a cada rodada infla o payload sem limite (Aula 2.4 já explicou o
porquê). O resumo é um retrato ESTRUTURADO e determinístico (fatos, decisões,
pendências, preferências), atualizado por regra explícita de transição de
estado — não uma cópia menor da transcrição.

Aula 2.8: o resumo passa a registrar também COMO cada turno foi resolvido
(`resolution_mode`) — regra determinística pura, componente local didático ou
fallback — pra deixar rastreável quando a resposta veio de cada caminho.
"""
from __future__ import annotations

from .generative import ResolutionMode
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

_FACT_TEMPLATE_BY_STATE: dict[ChatState, str] = {
    ChatState.SUPORTE_TECNICO: "Usuário informou problema técnico: {input}.",
    ChatState.FINANCEIRO: "Usuário informou referência de faturamento: {input}.",
    ChatState.INFORMACOES_CONTA: "Usuário solicitou consulta de conta: {input}.",
}

_ENCERRADO_DECISION = "Atendimento determinístico encerrado após coleta da informação."
_LOCAL_DIDACTIC_DECISION = "Atendimento encerrado após resposta do componente local didático."
_FALLBACK_DECISION = "Fallback determinístico acionado após indisponibilidade do componente local."


def _append_unique(items: list[str], value: str) -> None:
    if value and value not in items:
        items.append(value)


def _set_pending(summary: ConversationSummary, value: str | None) -> None:
    summary.pending.clear()
    if value:
        summary.pending.append(value)


def update_summary(
    session: Session,
    previous_state: ChatState,
    user_input: str,
    *,
    resolution_mode: ResolutionMode = ResolutionMode.DETERMINISTIC,
    resolved_state: ChatState | None = None,
) -> None:
    """Atualiza `session.summary` a partir da transição que acabou de
    acontecer (`previous_state` -> `session.state`). Regras por transição:

    - GREETING -> MAIN_MENU: só cria a pendência de escolher uma opção (a
      mensagem vazia de abertura não vira fato).
    - MAIN_MENU -> MAIN_MENU (entrada inválida OU texto livre não
      classificado com segurança): nenhum fato/decisão novos.
    - MAIN_MENU -> <área> (opção numérica OU texto livre reconhecido como
      handoff): registra a decisão de área selecionada + a pendência
      correspondente daquela área.
    - MAIN_MENU -> ENCERRADO (texto livre resolvido pelo componente local,
      `resolved_state` informado): registra a decisão de área selecionada +
      o fato da área resolvida + a decisão de encerramento via componente
      local + limpa a pendência.
    - <área> -> ENCERRADO: registra o fato com a mensagem do usuário
      (formulação "Usuário informou..." — nunca afirma que o dado é válido)
      + a decisão de encerramento (determinístico ou via componente local,
      conforme `resolution_mode`) + limpa a pendência.
    - <área> -> HUMAN_HANDOFF (fallback por indisponibilidade do componente):
      registra o fato + a decisão de fallback + a pendência de aguardar
      atendimento humano.
    - HUMAN_HANDOFF -> ENCERRADO: registra o fato da mensagem adicional e
      mantém a pendência de aguardar atendimento humano.
    - Mensagens depois de ENCERRADO: ignoradas (não alteram o resumo)."""
    summary = session.summary

    if previous_state == ChatState.GREETING and session.state == ChatState.MAIN_MENU:
        _set_pending(summary, _PENDING_BY_STATE[ChatState.MAIN_MENU])
        return

    if previous_state == ChatState.MAIN_MENU and session.state == ChatState.MAIN_MENU:
        return  # entrada inválida ou texto livre não classificado: nada novo

    if previous_state == ChatState.MAIN_MENU and session.state in _LABEL_BY_STATE:
        _append_unique(
            summary.decisions,
            f"Área de atendimento selecionada: {_LABEL_BY_STATE[session.state]}.",
        )
        _set_pending(summary, _PENDING_BY_STATE[session.state])
        return

    if (
        previous_state == ChatState.MAIN_MENU
        and session.state == ChatState.ENCERRADO
        and resolved_state in _FACT_TEMPLATE_BY_STATE
    ):
        _append_unique(
            summary.decisions,
            f"Área de atendimento selecionada: {_LABEL_BY_STATE[resolved_state]}.",
        )
        _append_unique(summary.facts, _FACT_TEMPLATE_BY_STATE[resolved_state].format(input=user_input))
        _append_unique(summary.decisions, _LOCAL_DIDACTIC_DECISION)
        _set_pending(summary, None)
        return

    if previous_state == ChatState.HUMAN_HANDOFF and session.state == ChatState.ENCERRADO:
        _append_unique(
            summary.facts,
            f"Usuário enviou informação adicional antes do atendimento humano: {user_input}.",
        )
        _set_pending(summary, _PENDING_BY_STATE[ChatState.HUMAN_HANDOFF])
        return

    if previous_state in _FACT_TEMPLATE_BY_STATE and session.state == ChatState.ENCERRADO:
        _append_unique(summary.facts, _FACT_TEMPLATE_BY_STATE[previous_state].format(input=user_input))
        decision = _LOCAL_DIDACTIC_DECISION if resolution_mode == ResolutionMode.LOCAL_DIDACTIC else _ENCERRADO_DECISION
        _append_unique(summary.decisions, decision)
        _set_pending(summary, None)
        return

    if previous_state in _FACT_TEMPLATE_BY_STATE and session.state == ChatState.HUMAN_HANDOFF:
        _append_unique(summary.facts, _FACT_TEMPLATE_BY_STATE[previous_state].format(input=user_input))
        _append_unique(summary.decisions, _FALLBACK_DECISION)
        _set_pending(summary, _PENDING_BY_STATE[ChatState.HUMAN_HANDOFF])
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
