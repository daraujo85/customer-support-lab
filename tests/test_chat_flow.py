from app.chat.flow import handle_input, menu_text, resolve_menu_option
from app.chat.state import ChatState, Session


def test_greeting_moves_to_main_menu_and_shows_options():
    session = Session()
    reply = handle_input(session, "")

    assert session.state == ChatState.MAIN_MENU
    assert "Suporte técnico" in reply


def test_valid_menu_option_transitions_to_expected_state():
    session = Session(state=ChatState.MAIN_MENU)
    reply = handle_input(session, "1")

    assert session.state == ChatState.SUPORTE_TECNICO
    assert "Suporte técnico" in reply


def test_invalid_menu_option_stays_on_main_menu():
    session = Session(state=ChatState.MAIN_MENU)
    reply = handle_input(session, "9")

    assert session.state == ChatState.MAIN_MENU
    assert reply.startswith("Não entendi.")


def test_menu_text_lists_all_options():
    text = menu_text()
    for label in ["Suporte técnico", "Questões de faturamento", "Informações de conta", "Falar com um atendente"]:
        assert label in text


def test_message_after_selected_option_ends_conversation():
    session = Session(state=ChatState.SUPORTE_TECNICO)

    reply = handle_input(session, "Meu computador não liga")

    assert session.state == ChatState.ENCERRADO
    assert "Obrigado pelo contato" in reply


def test_resolve_menu_option_returns_expected_option():
    option = resolve_menu_option("1")

    assert option is not None
    assert option.label == "Suporte técnico"
    assert option.next_state == ChatState.SUPORTE_TECNICO


def test_resolve_menu_option_ignores_surrounding_spaces():
    option = resolve_menu_option(" 1 ")

    assert option is not None
    assert option.next_state == ChatState.SUPORTE_TECNICO


def test_resolve_menu_option_returns_none_for_unknown_option():
    option = resolve_menu_option("9")

    assert option is None
