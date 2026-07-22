import pytest

import app.main as main_module
from app.chat.local_generation import LocalDidacticComponent
from app.chat.ollama_generation import OllamaGenerativeComponent
from app.chat.prompt_loader import PromptTemplateError
from app.main import build_generative_component


def test_local_didactic_mode(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "local_didactic")

    component = build_generative_component()

    assert isinstance(component, LocalDidacticComponent)


def test_default_mode_is_local_didactic(monkeypatch):
    monkeypatch.delenv("GENERATION_MODE", raising=False)

    component = build_generative_component()

    assert isinstance(component, LocalDidacticComponent)


def test_disabled_mode_returns_none(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "disabled")

    assert build_generative_component() is None


def test_ollama_mode_builds_component_with_defaults(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "ollama")
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("OLLAMA_NUM_CTX", raising=False)

    component = build_generative_component()

    assert isinstance(component, OllamaGenerativeComponent)
    assert component._base_url == "http://host.docker.internal:11434"
    assert component._model == "llama3.2:1b"
    assert component._num_ctx == 2048


def test_ollama_mode_reads_env_overrides(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://192.168.31.231:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "qwen3-vl:latest")
    monkeypatch.setenv("OLLAMA_TIMEOUT_SECONDS", "120")
    monkeypatch.setenv("OLLAMA_NUM_CTX", "4096")

    component = build_generative_component()

    assert component._base_url == "http://192.168.31.231:11434"
    assert component._model == "qwen3-vl:latest"
    assert component._num_ctx == 4096


def test_ollama_mode_invalid_timeout_raises(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "ollama")
    monkeypatch.setenv("OLLAMA_TIMEOUT_SECONDS", "0")

    with pytest.raises(ValueError):
        build_generative_component()


def test_ollama_mode_invalid_num_ctx_raises(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "ollama")
    monkeypatch.setenv("OLLAMA_NUM_CTX", "0")

    with pytest.raises(ValueError):
        build_generative_component()


def test_ollama_mode_empty_model_raises(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "ollama")
    monkeypatch.setenv("OLLAMA_MODEL", "")

    with pytest.raises(ValueError):
        build_generative_component()


def test_unknown_mode_raises(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "nao_existe")

    with pytest.raises(RuntimeError):
        build_generative_component()


def test_ollama_mode_fails_fast_when_prompt_artifact_is_invalid(monkeypatch):
    """Aula 3.9: artefato de prompt ausente/inválido é erro de CONFIGURAÇÃO —
    derruba o boot no modo ollama, diferente do Ollama estar desligado (isso
    é falha de serviço externo, tratada como fallback em runtime, não no boot)."""
    monkeypatch.setenv("GENERATION_MODE", "ollama")

    def _raise():
        raise PromptTemplateError("artefato de prompt ausente")

    monkeypatch.setattr(main_module, "load_prompt_template", _raise)

    with pytest.raises(PromptTemplateError):
        build_generative_component()


def test_local_didactic_mode_does_not_depend_on_prompt_artifact(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "local_didactic")

    def _raise():
        raise PromptTemplateError("não deveria ser chamado")

    monkeypatch.setattr(main_module, "load_prompt_template", _raise)

    component = build_generative_component()

    assert isinstance(component, LocalDidacticComponent)


def test_disabled_mode_does_not_depend_on_prompt_artifact(monkeypatch):
    monkeypatch.setenv("GENERATION_MODE", "disabled")

    def _raise():
        raise PromptTemplateError("não deveria ser chamado")

    monkeypatch.setattr(main_module, "load_prompt_template", _raise)

    assert build_generative_component() is None
