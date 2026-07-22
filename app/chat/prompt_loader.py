"""Carregamento do prompt como artefato versionado — Aula 3.9 do curso.

Até a Aula 3.8, a instrução de tarefa do `OllamaGenerativeComponent` vivia
como uma constante Python dentro de `ollama_generation.py`. Esta aula
extrai esse texto para `prompts/task_instruction.md` — um arquivo Markdown
versionado no git, revisável por Pull Request, com histórico e diff
próprios, independente do código que o consome.

O prompt NÃO é uma string auxiliar escondida no código. É um artefato de
comportamento, com histórico, revisão, testes e rollback.

Este módulo só lê e valida o arquivo — não decide QUANDO carregá-lo (isso
é responsabilidade de `app.main`, no ponto de composição da aplicação) nem
como renderizá-lo na chamada (isso continua em `ollama_generation.py`).
"""
from __future__ import annotations

from pathlib import Path
from string import Formatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TASK_INSTRUCTION_PATH = PROJECT_ROOT / "prompts" / "task_instruction.md"

_SUPPORTED_FIELDS = {"intent"}


class PromptTemplateError(RuntimeError):
    """Erro de configuração — o artefato de prompt é inválido ou está ausente.

    Fail-fast proposital: diferente de uma falha do Ollama (serviço externo
    indisponível, tratada como fallback determinístico), um artefato local
    ausente ou inválido é erro de configuração da própria aplicação — o
    modo `ollama` não deve subir com um prompt quebrado."""


def load_prompt_template(path: Path = DEFAULT_TASK_INSTRUCTION_PATH) -> str:
    """Lê, valida e devolve o template do prompt (ainda não renderizado).

    Validações: arquivo existe e é legível em UTF-8, não está vazio, declara
    o placeholder obrigatório `{intent}` e não declara nenhum placeholder
    que a aplicação não sabe preencher."""
    try:
        content = path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise PromptTemplateError(f"Não foi possível carregar o prompt: {path}") from exc
    except UnicodeDecodeError as exc:
        raise PromptTemplateError(f"O arquivo de prompt não está em UTF-8 válido: {path}") from exc

    if not content:
        raise PromptTemplateError(f"O arquivo de prompt está vazio: {path}")

    fields = {field_name for _, field_name, _, _ in Formatter().parse(content) if field_name}

    if "intent" not in fields:
        raise PromptTemplateError("O prompt precisa declarar o placeholder {intent}")

    unknown_fields = fields - _SUPPORTED_FIELDS
    if unknown_fields:
        raise PromptTemplateError(f"Placeholders não suportados: {sorted(unknown_fields)}")

    return content
