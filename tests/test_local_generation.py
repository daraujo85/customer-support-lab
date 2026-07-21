from app.chat.generative import Intent
from app.chat.local_generation import classify_intent, normalize_text


def test_normalize_removes_case_and_accents():
    assert normalize_text("COBRANÇA") == normalize_text("cobranca") == "cobranca"


def test_classifies_technical_message():
    turn = classify_intent("meu computador não liga")

    assert turn.intent == Intent.SUPORTE_TECNICO
    assert turn.score >= 0.70


def test_classifies_billing_message():
    turn = classify_intent("preciso da segunda via da fatura")

    assert turn.intent == Intent.FINANCEIRO
    assert turn.score >= 0.70


def test_classifies_account_message():
    turn = classify_intent("quero atualizar os dados da conta")

    assert turn.intent == Intent.INFORMACOES_CONTA
    assert turn.score >= 0.70


def test_identifies_human_handoff_request():
    turn = classify_intent("quero falar com atendente")

    assert turn.intent == Intent.HUMAN_HANDOFF


def test_returns_unknown_without_evidence():
    turn = classify_intent("bom dia, tudo bem?")

    assert turn.intent == Intent.UNKNOWN
    assert turn.score == 0.0


def test_returns_unknown_on_tie_between_intents():
    turn = classify_intent("conta e fatura")

    assert turn.intent == Intent.UNKNOWN


def test_expected_intent_skips_reclassification():
    from app.chat.local_generation import LocalDidacticComponent

    component = LocalDidacticComponent()
    turn = component.generate(
        messages=[],
        user_input="isso não tem nenhuma palavra-chave conhecida",
        expected_intent=Intent.FINANCEIRO,
    )

    assert turn.intent == Intent.FINANCEIRO
    assert turn.score == 1.0
    assert turn.reply
