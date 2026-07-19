from app.chat.flow import handle_input
from app.chat.payload import SYSTEM_PROMPT, build_payload
from app.chat.state import Session


def test_empty_session_payload_has_only_system_message():
    session = Session()

    payload = build_payload(session)

    assert payload == [{"role": "system", "content": SYSTEM_PROMPT}]


def test_payload_keeps_order_and_roles_after_a_round():
    session = Session()
    handle_input(session, "")  # greeting
    handle_input(session, "1")  # opção do menu

    payload = build_payload(session)

    roles = [item["role"] for item in payload]
    assert roles == ["system", "user", "assistant", "user", "assistant"]


def test_payload_content_matches_what_was_said():
    session = Session()
    greeting_reply = handle_input(session, "")
    option_reply = handle_input(session, "1")

    payload = build_payload(session)

    assert payload[1] == {"role": "user", "content": ""}
    assert payload[2] == {"role": "assistant", "content": greeting_reply}
    assert payload[3] == {"role": "user", "content": "1"}
    assert payload[4] == {"role": "assistant", "content": option_reply}


def test_every_payload_item_has_only_role_and_content_keys():
    session = Session()
    handle_input(session, "")

    payload = build_payload(session)

    for item in payload:
        assert set(item.keys()) == {"role", "content"}
