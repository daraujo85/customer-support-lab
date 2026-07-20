from app.chat.payload import build_payload
from app.chat.persona import (
    CUSTOMER_SUPPORT_PERSONA,
    build_system_prompt,
)
from app.chat.state import Session


def test_persona_has_explicit_contract():
    persona = CUSTOMER_SUPPORT_PERSONA

    assert persona.identity
    assert persona.scope
    assert persona.tone
    assert persona.vocabulary
    assert persona.boundaries


def test_system_prompt_has_explicit_sections():
    prompt = build_system_prompt(CUSTOMER_SUPPORT_PERSONA)

    assert "ESCOPO" in prompt
    assert "TOM" in prompt
    assert "VOCABULÁRIO" in prompt
    assert "LIMITES" in prompt


def test_system_prompt_declares_safety_boundaries():
    prompt = build_system_prompt(CUSTOMER_SUPPORT_PERSONA)

    assert "Não invente dados" in prompt
    assert "não aconteceram" in prompt
    assert "atendimento humano" in prompt


def test_payload_starts_with_rendered_persona():
    payload = build_payload(Session())

    assert payload[0] == {
        "role": "system",
        "content": build_system_prompt(CUSTOMER_SUPPORT_PERSONA),
    }
