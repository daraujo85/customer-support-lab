"""Montagem condicional do prompt — Aula 3.10 do curso.

Até a Aula 3.9, toda inferência real recebia exatamente a mesma instrução de
tarefa (`prompts/task_instruction.md`), não importa a intenção aceita. Esta
aula muda isso: o prompt enviado ao modelo passa a ser montado a partir de
DOIS pedaços — o template-base (comum a todas as áreas) e um bloco
específico da intenção já classificada (ver `chat.prompt_loader`).

A condição é escolhida pelo CÓDIGO, usando a intenção determinística já
aceita antes de chegar aqui (ver `chat.local_generation.classify_intent` e
`OllamaGenerativeComponent.generate`) — o modelo nunca escolhe qual bloco
usar, e nunca vê os blocos das outras áreas. Isso é o que os testes deste
módulo provam: nenhum vazamento de instrução entre áreas.

Este módulo é puro por design: nenhuma leitura de disco, nenhuma chamada de
rede, nenhum acesso a sessão, nenhuma classificação. Só recebe um
`PromptBundle` já carregado/validado e uma `Intent` já decidida, e devolve
uma string. Isso o torna trivial de testar sem mock nenhum.
"""
from __future__ import annotations

from .generative import Intent
from .prompt_loader import PromptBundle


class PromptAssemblyError(RuntimeError):
    """A intenção recebida não tem instrução específica cadastrada no bundle
    — por design, isso só deveria acontecer para `UNKNOWN`/`HUMAN_HANDOFF`
    (que nunca deveriam chegar até aqui) ou um bundle incompleto."""


def build_task_instruction(bundle: PromptBundle, intent: Intent) -> str:
    """Monta a instrução final: template-base renderizado + o bloco
    específico da área. Base sempre vem antes do bloco específico."""
    try:
        specific_instruction = bundle.intent_instructions[intent]
    except KeyError as exc:
        raise PromptAssemblyError(
            f"Não existe instrução para a intenção: {intent.value}"
        ) from exc

    base = bundle.task_template.format(intent=intent.value)

    return f"{base}\n\nORIENTAÇÕES DA ÁREA\n\n{specific_instruction}"
