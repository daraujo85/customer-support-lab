# Customer Support Lab

Laboratório evolutivo do curso [**Engenharia de Software na Era dos Agentes**](https://garagemdocodigo.com.br) — começa como um chatbot determinístico e evolui, aula a aula, até um ecossistema de agentes multimodal.

Domínio fictício (atendimento ao cliente genérico) — sem dado real de clientes ou negócio.

## Rodando

```bash
docker compose up --build
```

Depois abra `http://localhost:8010` no navegador.

Nenhuma instalação de Python ou dependência é necessária na sua máquina — tudo roda
dentro do container.

## Rodando os testes

```bash
docker compose run --rm app python -m pytest
```

## Estrutura

```
app/
  main.py          # FastAPI: serve a página + POST /api/chat
  chat/
    flow.py         # árvore de decisão determinística
    state.py        # estados, eventos e sessão
  static/           # HTML/CSS/JS do widget de chat
tests/              # pytest
docs/               # arquitetura + roadmap do laboratório por módulo
specs/              # Specs produzidas com a skill tlc-spec-driven (a partir do Módulo 3)
skills/             # skills/playbooks do curso
prompts/            # prompts como artefato versionado (a partir da Aula 3.9)
```

## Rodando com inferência real (Ollama)

```bash
GENERATION_MODE=ollama docker compose up --build
```

Requer [Ollama](https://ollama.com) rodando no host com o modelo baixado
(`ollama pull llama3.2:1b`). Variáveis de ambiente opcionais:
`OLLAMA_BASE_URL` (default `http://host.docker.internal:11434`),
`OLLAMA_MODEL` (default `llama3.2:1b`), `OLLAMA_TIMEOUT_SECONDS` (default
`60`), `OLLAMA_NUM_CTX` (default `2048`). Sem Ollama disponível, o app sobe
normalmente e cai no fallback determinístico na primeira chamada que falhar.

## Estado atual

**Aula 3.10** — o prompt passa a ser MONTADO condicionalmente: além do
template-base (`prompts/task_instruction.md`), cada intenção que gera
inferência real (suporte técnico, financeiro, informações de conta) tem um
bloco próprio em `prompts/intents/<intent>.md`. `app/chat/prompt_loader.py`
carrega os dois tipos num `PromptBundle`; o novo módulo puro
`app/chat/prompt_builder.py` seleciona o bloco certo (usando a intenção já
aceita pela classificação determinística) e monta a instrução final — o
modelo nunca escolhe qual bloco usar, e nunca vê os blocos das outras
áreas. `GENERATION_MODE=ollama` com qualquer artefato (base ou bloco)
ausente/inválido continua falhando rápido no boot. Ver
`specs/m03-a10-prompts-condicionais/spec.md`.

**Aula 3.9** — o prompt vira artefato versionado: a instrução de tarefa que
vivia como constante Python em `ollama_generation.py` agora mora em
`prompts/task_instruction.md`, carregada e validada por
`app/chat/prompt_loader.py` no ponto de composição da aplicação
(`app/main.py`). O texto e o comportamento são idênticos aos da Aula 3.8 —
só a ORIGEM mudou. `GENERATION_MODE=ollama` com o artefato ausente ou
inválido falha rápido no boot (erro de configuração); `local_didactic` e
`disabled` não dependem do arquivo. Ver
`specs/m03-a09-prompts-versionados/spec.md`.

**Aula 3.8** — primeira inferência REAL do laboratório: `GENERATION_MODE=ollama`
constrói `OllamaGenerativeComponent` (ver `app/chat/ollama_generation.py`,
Spec em `specs/m03-a08-contexto-em-camadas/spec.md`). Classificação de
intenção, score de confiança e transição de estado continuam 100%
determinísticos — só o TEXTO da resposta passa a vir de uma LLM local via
Ollama. `local_didactic` e `disabled` continuam funcionando exatamente como
antes. Ver `docs/architecture.md` para a evolução planejada módulo a módulo.
