"""Fluxo determinístico do chatbot (Aula 1.3): saudação por horário, menu fixo,
árvore de decisão, resposta final e encaminhamento humano. Zero geração de
linguagem — cada resposta é texto fixo escolhido por regra explícita.
"""
from __future__ import annotations

from datetime import datetime

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


def _resolve_reply(session: Session, user_input: str) -> str:
    """Aplica UMA transição da árvore de decisão e devolve a resposta fixa.

    Estado + evento (entrada do usuário) -> transição -> novo estado.
    Entrada não reconhecida não avança o estado (permanece no menu).
    """
    if session.state == ChatState.GREETING:
        session.state = ChatState.MAIN_MENU
        return f"{greeting()}\n\n{menu_text()}"

    if session.state == ChatState.MAIN_MENU:
        option = resolve_menu_option(user_input)
        if option is None:
            return "Não entendi. " + menu_text()
        session.state = option.next_state
        return _FIXED_RESPONSES[option.next_state]

    # Qualquer outro estado: encerra o atendimento determinístico.
    session.state = ChatState.ENCERRADO
    return "Obrigado pelo contato! Se precisar de algo mais, é só chamar de novo."


def handle_input(session: Session, user_input: str) -> str:
    """Resolve a transição e registra a rodada (user + assistant) na sessão
    no formato role/content — é esse registro que a Aula 2.1 expõe como o
    payload de conversação (ver `app/chat/payload.py`). Depois da transição,
    atualiza o resumo estruturado (Aula 2.5, ver `chat.summary`)."""
    user_input = user_input.strip()
    previous_state = session.state
    reply = _resolve_reply(session, user_input)

    session.messages.append(Message("user", user_input))
    session.messages.append(Message("assistant", reply))
    update_summary(session=session, previous_state=previous_state, user_input=user_input)
    return reply
