"""Carregamento do prompt como artefato versionado — Aulas 3.9 e 3.10 do curso.

Até a Aula 3.8, a instrução de tarefa do `OllamaGenerativeComponent` vivia
como uma constante Python dentro de `ollama_generation.py`. A Aula 3.9
extraiu esse texto para `prompts/task_instruction.md` — um arquivo Markdown
versionado no git, revisável por Pull Request, com histórico e diff
próprios, independente do código que o consome.

A Aula 3.10 adiciona um SEGUNDO tipo de artefato: uma instrução específica
por área (`prompts/intents/<intent>.md`) para cada intenção que de fato gera
inferência (suporte técnico, financeiro, informações de conta — nunca
`unknown`/`human_handoff`, que nunca chegam a montar prompt nenhum). Este
módulo carrega os dois tipos e devolve um `PromptBundle` imutável; a escolha
de QUAL bloco específico usar em cada chamada é responsabilidade de
`chat.prompt_builder`, não deste módulo.

O prompt NÃO é uma string auxiliar escondida no código. É um artefato de
comportamento, com histórico, revisão, testes e rollback.

Este módulo só lê e valida os arquivos — não decide QUANDO carregá-los (isso
é responsabilidade de `app.main`, no ponto de composição da aplicação) nem
como combiná-los/renderizá-los na chamada (isso é `chat.prompt_builder` e
`chat.ollama_generation`).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from string import Formatter
from typing import Mapping

from .generative import Intent

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TASK_INSTRUCTION_PATH = PROJECT_ROOT / "prompts" / "task_instruction.md"
_INTENTS_DIR = PROJECT_ROOT / "prompts" / "intents"

DEFAULT_INTENT_PROMPT_PATHS: Mapping[Intent, Path] = {
    Intent.SUPORTE_TECNICO: _INTENTS_DIR / "suporte_tecnico.md",
    Intent.FINANCEIRO: _INTENTS_DIR / "financeiro.md",
    Intent.INFORMACOES_CONTA: _INTENTS_DIR / "informacoes_conta.md",
}
"""Intenções que geram inferência real e por isso precisam de instrução
própria. `UNKNOWN` e `HUMAN_HANDOFF` ficam de fora de propósito — nunca
chegam a montar um prompt (ver `chat.ollama_generation.generate`)."""

_SUPPORTED_FIELDS = {"intent"}


class PromptTemplateError(RuntimeError):
    """Erro de configuração — o artefato de prompt é inválido ou está ausente.

    Fail-fast proposital: diferente de uma falha do Ollama (serviço externo
    indisponível, tratada como fallback determinístico), um artefato local
    ausente ou inválido é erro de configuração da própria aplicação — o
    modo `ollama` não deve subir com um prompt quebrado."""


@dataclass(frozen=True)
class PromptBundle:
    """Os artefatos de prompt já carregados e validados — pronto pra
    `chat.prompt_builder` selecionar e compor, sem tocar em disco de novo."""

    task_template: str
    intent_instructions: Mapping[Intent, str]


def _read_utf8(path: Path) -> str:
    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise PromptTemplateError(f"Não foi possível carregar o prompt: {path}") from exc
    except UnicodeDecodeError as exc:
        raise PromptTemplateError(f"O arquivo de prompt não está em UTF-8 válido: {path}") from exc

    if not content:
        raise PromptTemplateError(f"O arquivo de prompt está vazio: {path}")

    return content


def load_prompt_template(path: Path = DEFAULT_TASK_INSTRUCTION_PATH) -> str:
    """Lê, valida e devolve o template-base do prompt (ainda não renderizado).

    Validações: arquivo existe e é legível em UTF-8, não está vazio, declara
    o placeholder obrigatório `{intent}` e não declara nenhum placeholder
    que a aplicação não sabe preencher."""
    content = _read_utf8(path)

    fields = {field_name for _, field_name, _, _ in Formatter().parse(content) if field_name}

    if "intent" not in fields:
        raise PromptTemplateError("O prompt precisa declarar o placeholder {intent}")

    unknown_fields = fields - _SUPPORTED_FIELDS
    if unknown_fields:
        raise PromptTemplateError(f"Placeholders não suportados: {sorted(unknown_fields)}")

    return content


def _load_intent_instruction(intent: Intent, path: Path) -> str:
    """Lê e valida um bloco específico de área — diferente do template-base,
    ele NÃO declara nenhum placeholder (é texto final, já pronto pra ser
    anexado depois do template-base renderizado)."""
    content = _read_utf8(path)

    fields = {field_name for _, field_name, _, _ in Formatter().parse(content) if field_name}
    if fields:
        raise PromptTemplateError(
            f"O bloco de '{intent.value}' não deveria ter placeholders: {sorted(fields)}"
        )

    return content


def load_prompt_bundle(
    base_path: Path = DEFAULT_TASK_INSTRUCTION_PATH,
    intent_paths: Mapping[Intent, Path] = DEFAULT_INTENT_PROMPT_PATHS,
) -> PromptBundle:
    """Carrega o template-base e todos os blocos específicos por área,
    devolvendo um `PromptBundle` pronto pra `chat.prompt_builder`."""
    task_template = load_prompt_template(base_path)
    intent_instructions = {
        intent: _load_intent_instruction(intent, path) for intent, path in intent_paths.items()
    }
    return PromptBundle(task_template=task_template, intent_instructions=intent_instructions)
