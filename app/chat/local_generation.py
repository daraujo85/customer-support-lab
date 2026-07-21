"""Implementação LOCAL e didática do componente generativo — Aula 2.8.

`LocalDidacticComponent` é uma implementação REAL do contrato
`GenerativeComponent`, usada durante a execução normal do laboratório — não é
um mock de teste (os doubles de teste ficam em `tests/test_generative_flow.py`).

O que ela simula: a fronteira entre fluxo determinístico e componente de
interpretação, a classificação de intenção, um score de confiança, a geração
de uma resposta contextual, saída desconhecida e falha do componente.

O que ela NÃO simula: aleatoriedade. O score é calculado por regras e é
sempre reproduzível; a resposta é selecionada por template e é sempre
reproduzível. Nunca dizemos "a IA analisou a mensagem" — dizemos "o
componente local classificou a mensagem por regras didáticas".
"""
from __future__ import annotations

import unicodedata

from .generative import GeneratedTurn, GenerativeComponent, Intent, MessagePayload


def normalize_text(value: str) -> str:
    """Remove acentuação e caixa — permite reconhecer igualmente 'cobrança',
    'cobranca' e 'COBRANÇA'."""
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(character for character in normalized if not unicodedata.combining(character))


_INTENT_RULES: dict[Intent, dict[str, tuple[str, ...]]] = {
    Intent.SUPORTE_TECNICO: {
        "phrases": (
            "nao liga",
            "tela preta",
            "erro no sistema",
            "problema tecnico",
        ),
        "keywords": (
            "computador",
            "notebook",
            "tela",
            "erro",
            "travou",
            "internet",
            "aplicativo",
        ),
    },
    Intent.FINANCEIRO: {
        "phrases": (
            "cobranca duplicada",
            "segunda via",
            "valor incorreto",
        ),
        "keywords": (
            "fatura",
            "cobranca",
            "pagamento",
            "boleto",
            "reembolso",
            "pedido",
        ),
    },
    Intent.INFORMACOES_CONTA: {
        "phrases": (
            "alterar cadastro",
            "dados da conta",
            "mudar endereco",
        ),
        "keywords": (
            "conta",
            "cadastro",
            "email",
            "endereco",
            "telefone",
            "dados",
        ),
    },
    Intent.HUMAN_HANDOFF: {
        "phrases": (
            "falar com atendente",
            "falar com uma pessoa",
            "atendimento humano",
        ),
        "keywords": (
            "atendente",
            "humano",
        ),
    },
}
"""Lista pequena e fácil de explicar na aula — não é um sistema linguístico
completo. A limitação faz parte da demonstração."""


def _score_for_match(strong_phrase: bool, keyword_count: int) -> float:
    if strong_phrase:
        return 1.0
    if keyword_count >= 3:
        return 0.90
    if keyword_count == 2:
        return 0.80
    if keyword_count == 1:
        return 0.70
    return 0.0


def classify_intent(user_input: str) -> GeneratedTurn:
    """Classifica a entrada por regras determinísticas: normaliza, procura
    frases fortes, conta palavras-chave por intenção, calcula um score
    reproduzível e retorna UNKNOWN quando não há evidência suficiente ou em
    caso de empate entre intenções."""
    normalized_input = normalize_text(user_input)

    # Handoff tem prioridade quando uma frase forte de atendimento humano
    # está presente — mesmo que outra intenção também tenha evidência.
    handoff_rules = _INTENT_RULES[Intent.HUMAN_HANDOFF]
    if any(phrase in normalized_input for phrase in handoff_rules["phrases"]):
        return GeneratedTurn(
            intent=Intent.HUMAN_HANDOFF,
            score=1.0,
            reply="",
            matched_terms=(),
        )

    results: dict[Intent, tuple[float, tuple[str, ...]]] = {}
    for intent, rules in _INTENT_RULES.items():
        strong_phrase = next((p for p in rules["phrases"] if p in normalized_input), None)
        matched_keywords = tuple(k for k in rules["keywords"] if k in normalized_input)
        score = _score_for_match(strong_phrase is not None, len(matched_keywords))
        if score > 0:
            matched_terms = (strong_phrase,) if strong_phrase else matched_keywords
            results[intent] = (score, matched_terms)

    if not results:
        return GeneratedTurn(intent=Intent.UNKNOWN, score=0.0, reply="", matched_terms=())

    best_score = max(score for score, _ in results.values())
    winners = [intent for intent, (score, _) in results.items() if score == best_score]
    if len(winners) > 1:
        return GeneratedTurn(intent=Intent.UNKNOWN, score=0.0, reply="", matched_terms=())

    winner = winners[0]
    score, matched_terms = results[winner]
    return GeneratedTurn(intent=winner, score=score, reply="", matched_terms=matched_terms)


def generate_reply(intent: Intent, normalized_input: str, matched_terms: tuple[str, ...]) -> str:
    """Gera a resposta por template — nunca por geração livre de linguagem.
    Não gera texto para UNKNOWN nem HUMAN_HANDOFF (esses caminhos usam
    respostas fixas já existentes no fluxo)."""
    if intent == Intent.SUPORTE_TECNICO:
        if "tela" in normalized_input or "tela preta" in normalized_input:
            return (
                "Entendi que o problema envolve a tela. "
                "Verifique se o monitor recebe energia e se o cabo de vídeo está conectado."
            )
        return (
            "Entendi que o equipamento não está ligando. "
            "Verifique a alimentação e os cabos antes de continuar. "
            "Não compartilhe senhas ou dados sensíveis."
        )

    if intent == Intent.FINANCEIRO:
        return (
            "Entendi que sua dúvida é sobre faturamento. "
            "Informe o número do pedido ou da fatura, sem enviar dados completos de cartão."
        )

    if intent == Intent.INFORMACOES_CONTA:
        return (
            "Entendi que você precisa consultar dados da conta. "
            "Diga qual informação deseja consultar ou atualizar, sem compartilhar sua senha."
        )

    return ""


class LocalDidacticComponent:
    """Implementação concreta usada em runtime (ver `app.main`)."""

    def generate(
        self,
        *,
        messages: MessagePayload,
        user_input: str,
        expected_intent: Intent | None = None,
    ) -> GeneratedTurn:
        if expected_intent is not None:
            # O fluxo já sabe que está num domínio conhecido (ex.: usuário
            # escolheu "1" no menu) — não faz sentido reclassificar.
            reply = generate_reply(expected_intent, normalize_text(user_input), ())
            return GeneratedTurn(
                intent=expected_intent,
                score=1.0,
                reply=reply,
                matched_terms=(),
            )

        decision = classify_intent(user_input)
        if decision.intent in {Intent.UNKNOWN, Intent.HUMAN_HANDOFF}:
            return decision

        return GeneratedTurn(
            intent=decision.intent,
            score=decision.score,
            reply=generate_reply(decision.intent, normalize_text(user_input), decision.matched_terms),
            matched_terms=decision.matched_terms,
        )
