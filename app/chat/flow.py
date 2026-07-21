"""Fluxo do chatbot: saudação por horário, menu fixo, árvore de decisão,
resposta final e encaminhamento humano — tudo determinístico (Aula 1.3).

Aula 2.8: entrada livre no menu (e nos estados de domínio já conhecidos)
passa a poder ser resolvida por um `GenerativeComponent` (ver
`chat.generative`/`chat.local_generation`) — mas o CÓDIGO continua
responsável por validar o score, escolher o estado seguinte e acionar
fallback. O componente sugere; o código decide.
"""
from __future__ import annotations

from datetime import datetime

from .generative import (
    MIN_ACCEPTED_SCORE,
    GeneratedTurn,
    GenerativeComponent,
    GenerativeComponentError,
    Intent,
    ResolutionMode,
    build_generative_messages,
)
from .state import ChatState, MenuOption, Message, Session
from .summary import update_summary

MAIN_MENU: list[MenuOption] = [
    MenuOption("1", "Suporte técnico", ChatState.SUPORTE_TECNICO),
    MenuOption("2", "Questões de faturamento", ChatState.FINANCEIRO),
    MenuOption("3", "Informações de conta", ChatState.INFORMACOES_CONTA),
    MenuOption("4", "Falar com um atendente", ChatState.HUMAN_HANDOFF),
]

_FIXED_RESPONSES: dict[ChatState, str] = {
    ChatState.SUPORTE_TECNICO: (
        "Você está em Suporte técnico. Descreva o problema em poucas palavras "
        "que um atendente vai te responder em instantes."
    ),
    ChatState.FINANCEIRO: (
        "Você está em Questões de faturamento. Informe o número do seu pedido "
        "ou fatura para seguirmos."
    ),
    ChatState.INFORMACOES_CONTA: (
        "Você está em Informações de conta. Qual dado você precisa consultar?"
    ),
    ChatState.HUMAN_HANDOFF: (
        "Tudo bem, vou te encaminhar para um atendente humano. Aguarde um instante."
    ),
}

_HANDOFF_REPLY = _FIXED_RESPONSES[ChatState.HUMAN_HANDOFF]

CLASSIFICATION_FALLBACK_PREFIX = "Não consegui classificar sua mensagem com segurança. "
"""Usado quando o componente local retorna UNKNOWN, empate ou score abaixo de
MIN_ACCEPTED_SCORE — o fluxo permanece no menu, sem inventar uma resposta."""

INTENT_TO_STATE: dict[Intent, ChatState] = {
    Intent.SUPORTE_TECNICO: ChatState.SUPORTE_TECNICO,
    Intent.FINANCEIRO: ChatState.FINANCEIRO,
    Intent.INFORMACOES_CONTA: ChatState.INFORMACOES_CONTA,
    Intent.HUMAN_HANDOFF: ChatState.HUMAN_HANDOFF,
}
"""O componente sugere a intenção. O código escolhe o estado — esta tabela é
a única responsável por essa conversão."""

_STATE_TO_INTENT: dict[ChatState, Intent] = {
    ChatState.SUPORTE_TECNICO: Intent.SUPORTE_TECNICO,
    ChatState.FINANCEIRO: Intent.FINANCEIRO,
    ChatState.INFORMACOES_CONTA: Intent.INFORMACOES_CONTA,
}
"""Estados de domínio já conhecidos (usuário escolheu uma opção numérica) —
usado pra passar `expected_intent` ao componente sem reclassificar."""


def greeting() -> str:
    """Saudação baseada no horário do sistema — sem IA, só relógio."""
    hour = datetime.now().hour
    if hour < 12:
        period = "Bom dia"
    elif hour < 18:
        period = "Boa tarde"
    else:
        period = "Boa noite"
    return f"{period}! Bem-vindo ao suporte. Como posso te ajudar hoje?"


def menu_text() -> str:
    lines = [f"{opt.key}. {opt.label}" for opt in MAIN_MENU]
    return "Escolha uma opção:\n" + "\n".join(lines)


def resolve_menu_option(user_input: str) -> MenuOption | None:
    """Regra de domínio: resolve qual opção do menu corresponde à entrada
    do usuário (ou None se não houver correspondência)."""
    normalized_input = user_input.strip()
    return next(
        (option for option in MAIN_MENU if option.key == normalized_input),
        None,
    )


def _classify_free_text(
    session: Session, user_input: str, component: GenerativeComponent | None
) -> GeneratedTurn | None:
    """Chama o componente pra classificar texto livre no menu principal.
    Retorna None quando não há componente disponível (fluxo trata como
    UNKNOWN/fallback)."""
    if component is None:
        return None
    messages = build_generative_messages(session, user_input)
    try:
        return component.generate(messages=messages, user_input=user_input)
    except GenerativeComponentError:
        return None


def _resolve_reply(
    session: Session, user_input: str, component: GenerativeComponent | None
) -> tuple[str, ResolutionMode, ChatState | None]:
    """Aplica UMA transição da árvore de decisão e devolve a resposta, o modo
    de resolução (pra registrar no resumo) e o estado de domínio resolvido
    (quando a transição pulou direto pra ENCERRADO via componente local)."""
    if session.state == ChatState.GREETING:
        session.state = ChatState.MAIN_MENU
        return f"{greeting()}\n\n{menu_text()}", ResolutionMode.DETERMINISTIC, None

    if session.state == ChatState.MAIN_MENU:
        option = resolve_menu_option(user_input)
        if option is not None:
            session.state = option.next_state
            return _FIXED_RESPONSES[option.next_state], ResolutionMode.DETERMINISTIC, None

        # Entrada não é uma opção numérica: tenta classificar como texto livre.
        turn = _classify_free_text(session, user_input, component)
        if turn is None or turn.intent == Intent.UNKNOWN or turn.score < MIN_ACCEPTED_SCORE:
            return CLASSIFICATION_FALLBACK_PREFIX + menu_text(), ResolutionMode.FALLBACK, None

        next_state = INTENT_TO_STATE[turn.intent]
        if turn.intent == Intent.HUMAN_HANDOFF:
            session.state = next_state
            return _HANDOFF_REPLY, ResolutionMode.LOCAL_DIDACTIC, None

        session.state = ChatState.ENCERRADO
        return turn.reply, ResolutionMode.LOCAL_DIDACTIC, next_state

    if session.state in _STATE_TO_INTENT:
        # Estado de domínio já conhecido: chama o componente com a intenção
        # esperada (não reclassifica) e valida a resposta antes de encerrar.
        expected_intent = _STATE_TO_INTENT[session.state]
        turn: GeneratedTurn | None = None
        if component is not None:
            messages = build_generative_messages(session, user_input)
            try:
                turn = component.generate(
                    messages=messages, user_input=user_input, expected_intent=expected_intent
                )
            except GenerativeComponentError:
                turn = None

        if turn is None:
            session.state = ChatState.HUMAN_HANDOFF
            return _HANDOFF_REPLY, ResolutionMode.FALLBACK, None

        session.state = ChatState.ENCERRADO
        return turn.reply, ResolutionMode.LOCAL_DIDACTIC, None

    # HUMAN_HANDOFF ou ENCERRADO: encerramento determinístico, sem componente.
    session.state = ChatState.ENCERRADO
    return (
        "Obrigado pelo contato! Se precisar de algo mais, é só chamar de novo.",
        ResolutionMode.DETERMINISTIC,
        None,
    )


def handle_input(
    session: Session, user_input: str, component: GenerativeComponent | None = None
) -> str:
    """Resolve a transição e registra a rodada (user + assistant) na sessão
    no formato role/content — é esse registro que a Aula 2.1 expõe como o
    payload de conversação (ver `app/chat/payload.py`). Depois da transição,
    atualiza o resumo estruturado (Aula 2.5, ver `chat.summary`).

    `component`: implementação de `GenerativeComponent` usada pra resolver
    texto livre (Aula 2.8) — `None` desliga a camada generativa por completo
    (texto livre sempre cai no fallback determinístico do menu)."""
    user_input = user_input.strip()
    previous_state = session.state
    reply, resolution_mode, resolved_state = _resolve_reply(session, user_input, component)

    session.messages.append(Message("user", user_input))
    session.messages.append(Message("assistant", reply))
    update_summary(
        session=session,
        previous_state=previous_state,
        user_input=user_input,
        resolution_mode=resolution_mode,
        resolved_state=resolved_state,
    )
    return reply
