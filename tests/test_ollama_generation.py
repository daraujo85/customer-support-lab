import httpx
import pytest

from app.chat.generative import GenerativeComponentError, Intent
from app.chat.ollama_generation import OllamaGenerativeComponent


def _component(handler) -> OllamaGenerativeComponent:
    """Monta o componente com um `httpx.MockTransport` — nenhuma chamada de
    rede real acontece nestes testes."""
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return OllamaGenerativeComponent(
        base_url="http://ollama.local:11434",
        model="llama3.2:1b",
        timeout_seconds=30,
        num_ctx=2048,
        client=client,
    )


def _ok_response(content: str) -> httpx.Response:
    return httpx.Response(200, json={"message": {"role": "assistant", "content": content}})


def test_calls_chat_endpoint_with_model_options_and_task_instruction():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        import json

        captured["url"] = str(request.url)
        captured["json"] = json.loads(request.content)
        return _ok_response("Sua fatura está em análise.")

    component = _component(handler)
    messages = [{"role": "system", "content": "persona"}, {"role": "user", "content": "minha fatura veio errada"}]

    turn = component.generate(messages=messages, user_input="minha fatura veio errada")

    assert captured["url"] == "http://ollama.local:11434/api/chat"
    payload = captured["json"]
    assert payload["model"] == "llama3.2:1b"
    assert payload["stream"] is False
    assert payload["options"] == {"temperature": 0, "seed": 42, "num_ctx": 2048}
    assert payload["messages"][:2] == messages
    assert payload["messages"][-1]["role"] == "system"
    assert "financeiro" in payload["messages"][-1]["content"]
    assert turn.source == "ollama"
    assert turn.reply == "Sua fatura está em análise."
    assert turn.intent == Intent.FINANCEIRO


def test_valid_response_preserves_deterministic_intent_and_score():
    component = _component(lambda request: _ok_response("Resposta qualquer."))

    turn = component.generate(messages=[], user_input="meu computador não liga")

    assert turn.intent == Intent.SUPORTE_TECNICO
    assert turn.score == 1.0
    assert turn.source == "ollama"


def test_expected_intent_skips_reclassification_and_calls_model():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return _ok_response("Vamos verificar sua conexão.")

    component = _component(handler)

    turn = component.generate(
        messages=[], user_input="ainda não voltou", expected_intent=Intent.SUPORTE_TECNICO
    )

    assert len(calls) == 1
    assert turn.intent == Intent.SUPORTE_TECNICO
    assert turn.score == 1.0
    assert turn.matched_terms == ()
    assert turn.reply == "Vamos verificar sua conexão."


def test_unknown_intent_does_not_call_network():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return _ok_response("não deveria chegar aqui")

    component = _component(handler)

    turn = component.generate(messages=[], user_input="bom dia")

    assert calls == []
    assert turn.intent == Intent.UNKNOWN
    assert turn.source == "local_didactic"


def test_human_handoff_does_not_call_network():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return _ok_response("não deveria chegar aqui")

    component = _component(handler)

    turn = component.generate(messages=[], user_input="quero falar com atendente")

    assert calls == []
    assert turn.intent == Intent.HUMAN_HANDOFF


def test_connection_error_raises_generative_component_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("recusado", request=request)

    component = _component(handler)

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_timeout_raises_generative_component_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timeout", request=request)

    component = _component(handler)

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_bad_status_raises_generative_component_error():
    component = _component(lambda request: httpx.Response(500, text="erro interno"))

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_malformed_body_raises_generative_component_error():
    component = _component(lambda request: httpx.Response(200, text="isso não é json"))

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_missing_message_field_raises_generative_component_error():
    component = _component(lambda request: httpx.Response(200, json={"done": True}))

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_empty_content_raises_generative_component_error():
    component = _component(lambda request: _ok_response("   "))

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_oversized_content_raises_generative_component_error():
    component = _component(lambda request: _ok_response("x" * 2001))

    with pytest.raises(GenerativeComponentError):
        component.generate(messages=[], user_input="minha fatura veio errada")


def test_constructor_validates_arguments():
    with pytest.raises(ValueError):
        OllamaGenerativeComponent(base_url="", model="m", timeout_seconds=1)
    with pytest.raises(ValueError):
        OllamaGenerativeComponent(base_url="http://x", model="", timeout_seconds=1)
    with pytest.raises(ValueError):
        OllamaGenerativeComponent(base_url="http://x", model="m", timeout_seconds=0)
    with pytest.raises(ValueError):
        OllamaGenerativeComponent(base_url="http://x", model="m", timeout_seconds=1, num_ctx=0)
