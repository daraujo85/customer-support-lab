from app.chat.flow import _HANDOFF_REPLY, handle_input
from app.chat.generative import GeneratedTurn, GenerativeComponentError, Intent
from app.chat.state import ChatState, Session


class SpyGenerativeComponent:
    """Double de teste — NÃO é a implementação usada pela aplicação (essa é
    `LocalDidacticComponent`, ver `chat.local_generation`)."""

    def __init__(self, turn: GeneratedTurn):
        self.turn = turn
        self.calls: list[dict] = []

    def generate(self, *, messages, user_input, expected_intent=None):
        self.calls.append({"messages": messages, "user_input": user_input, "expected_intent": expected_intent})
        return self.turn


class FailingGenerativeComponent:
    """Double de teste que simula indisponibilidade do componente."""

    def generate(self, *, messages, user_input, expected_intent=None):
        raise GenerativeComponentError("componente indisponível")


def test_greeting_does_not_call_component():
    session = Session()
    spy = SpyGenerativeComponent(GeneratedTurn(Intent.UNKNOWN, 0.0, "", ()))

    handle_input(session, "", component=spy)

    assert spy.calls == []


def test_numeric_option_does_not_call_component():
    session = Session(state=ChatState.MAIN_MENU)
    spy = SpyGenerativeComponent(GeneratedTurn(Intent.UNKNOWN, 0.0, "", ()))

    reply = handle_input(session, "1", component=spy)

    assert spy.calls == []
    assert session.state == ChatState.SUPORTE_TECNICO
    assert "Suporte técnico" in reply


def test_recognized_free_text_generates_reply_and_ends_flow():
    session = Session(state=ChatState.MAIN_MENU)
    turn = GeneratedTurn(Intent.FINANCEIRO, 0.90, "Entendi que sua dúvida é sobre faturamento.", ("fatura",))
    component = SpyGenerativeComponent(turn)

    reply = handle_input(session, "minha fatura veio errada", component=component)

    assert session.state == ChatState.ENCERRADO
    assert reply == turn.reply


def test_recognized_free_text_records_fact_decision_and_preserves_history():
    session = Session(state=ChatState.MAIN_MENU)
    turn = GeneratedTurn(Intent.FINANCEIRO, 0.90, "Entendi que sua dúvida é sobre faturamento.", ("fatura",))
    component = SpyGenerativeComponent(turn)

    handle_input(session, "minha fatura veio errada", component=component)

    assert "Área de atendimento selecionada: Questões de faturamento." in session.summary.decisions
    assert any("fatura" in fact for fact in session.summary.facts)
    assert "Atendimento encerrado após resposta do componente local didático." in session.summary.decisions
    assert len(session.messages) == 2  # histórico bruto preservado (user + assistant)


def test_unknown_intent_keeps_menu_state_and_uses_fallback():
    session = Session(state=ChatState.MAIN_MENU)
    component = SpyGenerativeComponent(GeneratedTurn(Intent.UNKNOWN, 0.0, "", ()))

    reply = handle_input(session, "bom dia", component=component)

    assert session.state == ChatState.MAIN_MENU
    assert reply.startswith("Não consegui classificar sua mensagem com segurança.")
    assert session.summary.decisions == []


def test_handoff_intent_uses_fixed_response():
    session = Session(state=ChatState.MAIN_MENU)
    component = SpyGenerativeComponent(GeneratedTurn(Intent.HUMAN_HANDOFF, 1.0, "", ()))

    reply = handle_input(session, "quero falar com atendente", component=component)

    assert session.state == ChatState.HUMAN_HANDOFF
    assert reply == _HANDOFF_REPLY


def test_disabled_component_in_menu_uses_fallback():
    session = Session(state=ChatState.MAIN_MENU)

    reply = handle_input(session, "meu computador não liga", component=None)

    assert session.state == ChatState.MAIN_MENU
    assert reply.startswith("Não consegui classificar sua mensagem com segurança.")


def test_unavailable_component_in_domain_triggers_handoff_and_updates_summary():
    session = Session(state=ChatState.SUPORTE_TECNICO)
    component = FailingGenerativeComponent()

    reply = handle_input(session, "meu computador não liga", component=component)

    assert session.state == ChatState.HUMAN_HANDOFF
    assert reply == _HANDOFF_REPLY
    assert "Fallback determinístico acionado após indisponibilidade do componente local." in session.summary.decisions
    assert session.summary.pending == ["Aguardar atendimento humano."]


def test_ollama_turn_ends_flow_and_summary_registers_ollama_mode():
    """Aula 3.8: turno com source='ollama' encerra o fluxo normalmente e o
    resumo registra a decisão específica de Ollama, distinta da do
    componente local didático."""
    session = Session(state=ChatState.MAIN_MENU)
    turn = GeneratedTurn(
        Intent.FINANCEIRO,
        0.90,
        "Sua fatura está em análise, aguarde o retorno.",
        ("fatura",),
        source="ollama",
    )
    component = SpyGenerativeComponent(turn)

    reply = handle_input(session, "minha fatura veio errada", component=component)

    assert session.state == ChatState.ENCERRADO
    assert reply == turn.reply
    assert "Atendimento encerrado após resposta do modelo local via Ollama." in session.summary.decisions
    assert "Atendimento encerrado após resposta do componente local didático." not in session.summary.decisions


def test_ollama_turn_in_known_domain_ends_flow_with_ollama_mode():
    session = Session(state=ChatState.SUPORTE_TECNICO)
    turn = GeneratedTurn(
        Intent.SUPORTE_TECNICO,
        1.0,
        "Vamos verificar a conexão do seu equipamento.",
        (),
        source="ollama",
    )
    component = SpyGenerativeComponent(turn)

    reply = handle_input(session, "meu computador não liga", component=component)

    assert session.state == ChatState.ENCERRADO
    assert reply == turn.reply
    assert "Atendimento encerrado após resposta do modelo local via Ollama." in session.summary.decisions


def test_component_failure_still_triggers_fallback_regardless_of_ollama_mode():
    """Falha do componente (Ollama fora do ar, por exemplo) continua caindo
    no mesmo fallback determinístico já usado pro componente local."""
    session = Session(state=ChatState.SUPORTE_TECNICO)
    component = FailingGenerativeComponent()

    reply = handle_input(session, "meu computador não liga", component=component)

    assert session.state == ChatState.HUMAN_HANDOFF
    assert reply == _HANDOFF_REPLY


def test_numeric_option_still_does_not_call_component_with_ollama_double():
    """O caminho numérico nunca chama o componente, independente de qual
    implementação está configurada (local didática ou Ollama)."""
    session = Session(state=ChatState.MAIN_MENU)
    turn = GeneratedTurn(Intent.UNKNOWN, 0.0, "", (), source="ollama")
    component = SpyGenerativeComponent(turn)

    reply = handle_input(session, "1", component=component)

    assert component.calls == []
    assert session.state == ChatState.SUPORTE_TECNICO
    assert "Suporte técnico" in reply
