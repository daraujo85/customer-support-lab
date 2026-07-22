import pytest

from app.chat.prompt_loader import PromptTemplateError, load_prompt_template


def test_loads_the_official_prompt_artifact():
    template = load_prompt_template()

    assert template.strip()
    assert "{intent}" in template


def test_official_prompt_contains_security_rules():
    template = load_prompt_template()

    assert "Não reclassifique a intenção" in template
    assert "senha" in template.lower()
    assert "credenciais" in template.lower()


def test_official_prompt_renders_with_a_known_intent():
    template = load_prompt_template()

    rendered = template.format(intent="financeiro")

    assert "financeiro" in rendered
    assert "{intent}" not in rendered


def test_missing_file_raises_prompt_template_error(tmp_path):
    missing = tmp_path / "does_not_exist.md"

    with pytest.raises(PromptTemplateError):
        load_prompt_template(missing)


def test_empty_file_raises_prompt_template_error(tmp_path):
    empty = tmp_path / "empty.md"
    empty.write_text("", encoding="utf-8")

    with pytest.raises(PromptTemplateError):
        load_prompt_template(empty)


def test_file_without_intent_placeholder_raises(tmp_path):
    no_placeholder = tmp_path / "no_placeholder.md"
    no_placeholder.write_text("Responda de forma educada.", encoding="utf-8")

    with pytest.raises(PromptTemplateError):
        load_prompt_template(no_placeholder)


def test_unknown_placeholder_raises(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("A área é {intent}. O usuário é {user_name}.", encoding="utf-8")

    with pytest.raises(PromptTemplateError):
        load_prompt_template(bad)


def test_invalid_utf8_raises_prompt_template_error(tmp_path):
    bad_encoding = tmp_path / "bad_encoding.md"
    bad_encoding.write_bytes(b"\xff\xfe area {intent}")

    with pytest.raises(PromptTemplateError):
        load_prompt_template(bad_encoding)


def test_rendered_prompt_is_identical_to_previous_inline_version():
    """Prova a afirmação central da aula: a origem mudou, o comportamento não —
    esse é exatamente o texto que vivia embutido em ollama_generation.py na 3.8."""
    template = load_prompt_template()

    rendered = template.format(intent="financeiro")

    assert rendered == (
        "TAREFA ATUAL\n\n"
        "A área já foi determinada pelo sistema como: financeiro.\n"
        "Não reclassifique a intenção.\n"
        "Responda em português do Brasil.\n"
        "Use no máximo três frases.\n"
        "Não peça senha, cartão completo ou credenciais.\n"
        "Não invente dados que não aparecem no contexto."
    )
