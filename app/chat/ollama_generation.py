"""Implementação REAL de inferência via Ollama — Aula 3.8 do curso.

`OllamaGenerativeComponent` implementa o mesmo `Protocol GenerativeComponent`
do componente local didático (`chat.local_generation`), mas o TEXTO da
resposta agora vem de uma LLM de verdade, rodando localmente via Ollama.

O que muda: a resposta.
O que NÃO muda: a classificação de intenção continua 100% determinística
(`classify_intent`, de `chat.local_generation`) — o Ollama só é chamado
depois que essa classificação já aceitou uma intenção (ou quando o domínio
já é conhecido, via `expected_intent`). A LLM escreve a frase; o código
continua decidindo quando chamá-la, qual intenção foi aceita, qual estado
muda e o que acontece quando ela falha (fallback determinístico, igual ao
componente local didático).

Ver a Spec desta aula em
`specs/m03-a08-contexto-em-camadas/spec.md` pro raciocínio completo por
trás dessas decisões (por que não pedir intent+confidence ao modelo, por
que sem retry, o que fica probabilístico e o que continua determinístico).

Aula 3.9: a instrução de tarefa deixa de ser uma constante Python neste
arquivo — agora é injetada no construtor (`task_instruction_template`),
já carregada e validada por `chat.prompt_loader` no ponto de composição
da aplicação (`app.main`). Este módulo só RENDERIZA o template recebido;
não conhece caminho de arquivo nenhum. Ver
`specs/m03-a09-prompts-versionados/spec.md`.
"""
from __future__ import annotations

import httpx

from .generative import GeneratedTurn, GenerativeComponentError, Intent, MessagePayload
from .local_generation import classify_intent

_MAX_REPLY_CHARS = 2000
"""Limite defensivo — uma resposta anormalmente grande é tratada como falha,
não como sucesso parcial."""


def _add_task_instruction(messages: MessagePayload, intent: Intent, template: str) -> MessagePayload:
    """Insere a instrução de tarefa (já RENDERIZADA a partir de `template`)
    ANTES da última mensagem (a do usuário), nunca depois — terminar a lista
    numa mensagem `system` quebra o template de chat do modelo (o Llama
    espera que o turno mais recente seja do usuário) e faz o modelo devolver
    os marcadores de template como texto (`<|start_header_id|>...`) em vez
    de só a resposta."""
    instruction = template.format(intent=intent.value)
    return [*messages[:-1], {"role": "system", "content": instruction}, *messages[-1:]]


def _extract_reply(response: httpx.Response) -> str:
    if response.status_code != 200:
        raise GenerativeComponentError(
            f"Ollama respondeu HTTP {response.status_code}: {response.text[:200]}"
        )
    try:
        data = response.json()
    except ValueError as exc:
        raise GenerativeComponentError("Resposta do Ollama não é JSON válido") from exc

    message = data.get("message")
    if not isinstance(message, dict):
        raise GenerativeComponentError("Resposta do Ollama sem campo 'message'")

    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise GenerativeComponentError("Resposta do Ollama com 'content' vazio")

    if len(content) > _MAX_REPLY_CHARS:
        raise GenerativeComponentError("Resposta do Ollama excedeu o limite defensivo de tamanho")

    return content.strip()


class OllamaGenerativeComponent:
    """Implementação concreta usada em runtime quando
    `GENERATION_MODE=ollama` (ver `app.main`).

    `client`: injeção opcional de um `httpx.Client` — permite usar um
    transporte falso (`httpx.MockTransport`) nos testes, sem abrir conexão
    de rede real.

    `task_instruction_template`: o template JÁ carregado e validado (ver
    `chat.prompt_loader.load_prompt_template`) — este componente só
    renderiza, nunca lê arquivo."""

    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        timeout_seconds: float,
        task_instruction_template: str,
        num_ctx: int = 2048,
        client: httpx.Client | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url não pode ser vazio")
        if not model:
            raise ValueError("model não pode ser vazio")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds precisa ser maior que zero")
        if num_ctx <= 0:
            raise ValueError("num_ctx precisa ser maior que zero")
        if not task_instruction_template:
            raise ValueError("task_instruction_template não pode ser vazio")

        self._base_url = base_url.rstrip("/")
        self._model = model
        self._num_ctx = num_ctx
        self._task_instruction_template = task_instruction_template
        self._client = client or httpx.Client(timeout=timeout_seconds)

    def generate(
        self,
        *,
        messages: MessagePayload,
        user_input: str,
        expected_intent: Intent | None = None,
    ) -> GeneratedTurn:
        if expected_intent is not None:
            # Domínio já conhecido: não reclassifica, só gera a resposta.
            intent = expected_intent
            score = 1.0
            matched_terms: tuple[str, ...] = ()
        else:
            decision = classify_intent(user_input)
            if decision.intent in {Intent.UNKNOWN, Intent.HUMAN_HANDOFF}:
                # Nenhuma chamada de rede — o fluxo trata esses casos sem LLM.
                return decision
            intent = decision.intent
            score = decision.score
            matched_terms = decision.matched_terms

        request_messages = _add_task_instruction(messages, intent, self._task_instruction_template)
        try:
            response = self._client.post(
                f"{self._base_url}/api/chat",
                json={
                    "model": self._model,
                    "messages": request_messages,
                    "stream": False,
                    "options": {
                        "temperature": 0,
                        "seed": 42,
                        "num_ctx": self._num_ctx,
                    },
                },
            )
        except httpx.RequestError as exc:
            raise GenerativeComponentError(f"Falha de conexão com o Ollama: {exc}") from exc

        reply = _extract_reply(response)

        return GeneratedTurn(
            intent=intent,
            score=score,
            reply=reply,
            matched_terms=matched_terms,
            source="ollama",
        )
