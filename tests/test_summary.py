from app.chat.flow import handle_input
from app.chat.payload import RECENT_MESSAGE_LIMIT, build_payload
from app.chat.state import Session
from app.chat.summary import render_summary


def test_greeting_creates_pending_to_choose_an_option():
    session = Session()
    handle_input(session, "")

    assert session.summary.pending == ["Escolher uma opção de atendimento."]


def test_valid_menu_option_registers_decision_and_new_pending():
    session = Session()
    handle_input(session, "")
    handle_input(session, "1")

    assert "Suporte técnico" in session.summary.decisions[0]
    assert session.summary.pending == ["Descrever o problema técnico."]


def test_invalid_menu_option_creates_no_decision():
    session = Session()
    handle_input(session, "")
    handle_input(session, "9")

    assert session.summary.decisions == []


def test_technical_information_becomes_fact_and_clears_pending():
    session = Session()
    handle_input(session, "")
    handle_input(session, "1")
    handle_input(session, "meu computador não liga")

    assert session.summary.facts == ["Usuário informou problema técnico: meu computador não liga."]
    assert session.summary.pending == []


def test_human_handoff_keeps_pending_even_after_extra_message():
    session = Session()
    handle_input(session, "")
    handle_input(session, "4")
    handle_input(session, "mais um detalhe")

    assert session.summary.pending == ["Aguardar atendimento humano."]


def test_preferences_are_never_inferred():
    session = Session()
    handle_input(session, "")
    handle_input(session, "1")
    handle_input(session, "meu computador não liga")

    assert session.summary.preferences == []
    assert "Nenhuma preferência explícita registrada." in render_summary(session.summary)


def test_short_payload_stays_unchanged():
    session = Session()
    handle_input(session, "")  # greeting
    handle_input(session, "1")  # opção -> 4 mensagens (== limite, sem compactar)

    payload = build_payload(session)

    roles = [item["role"] for item in payload]
    assert roles == ["system", "user", "assistant", "user", "assistant"]


def test_long_payload_gets_compacted_but_raw_history_is_preserved():
    session = Session()
    handle_input(session, "")
    handle_input(session, "1")
    handle_input(session, "meu computador não liga")  # 6 mensagens -> compacta

    payload = build_payload(session)

    assert payload[0]["role"] == "system"
    assert "CONTEXTO RESUMIDO DA SESSÃO" in payload[0]["content"]
    assert len(payload) == RECENT_MESSAGE_LIMIT + 1
    assert len(session.messages) == 6  # histórico bruto nunca é apagado
