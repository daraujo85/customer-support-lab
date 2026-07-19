# Aula 2.1 — O que existe por trás de um chat

```text
Branch: lesson/m02-a01-payload-conversacao
Base: tag m01-a06-end (main estava à frente com commits de docs/fotonovela
      sem relação com o laboratório — derivado da tag, não da main, seguindo
      a regra do próprio docs/workflow-git.md)
Alteração no laboratório: exposição e visualização do payload de mensagens
Commit: 6 commits pequenos, mergeados --no-ff na main
```

## Objetivo prático

Até a Aula 1.6, `Session.history` guardava só o texto bruto que o usuário
digitava — nem a resposta do bot era registrada. Não existia (e ainda não
existe) nenhuma chamada de LLM no projeto; isso só chega na Aula 2.8. O
objetivo desta aula é fazer o aluno **enxergar** a estrutura que qualquer API
de chat (OpenAI, Anthropic, etc.) espera receber — uma lista ordenada de
mensagens com **papel** (`system`/`user`/`assistant`) e **conteúdo** — antes
mesmo de qualquer geração acontecer. "Um chat não é mágica, é uma lista de
mensagens."

## O que foi alterado (só isto)

```text
app/chat/state.py       — Message (role/content) + Session.messages (era Session.history)
app/chat/flow.py        — handle_input passa a registrar cada rodada (user+assistant)
app/chat/payload.py     — NOVO: build_payload(session) monta o payload role/content
app/main.py             — NOVO endpoint GET /api/chat/{session_id}/payload
app/static/index.html   — botão "Ver payload" + painel <pre>
app/static/app.js       — busca e exibe o payload (atualiza a cada mensagem)
app/static/styles.css   — estilo do painel de payload
tests/test_payload.py   — NOVO: 4 testes de build_payload
```

Confirmado via `git diff --stat m02-a01-start m02-a01-end`: nenhum arquivo de
config (`Dockerfile`, `docker-compose.yml`, `pyproject.toml`) mudou — zero
dependência nova.

## As 6 etapas reais (6 commits)

**1. `feat: adiciona Message estruturada e lista de mensagens à Session`**
```python
@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: str
```
`Session.history: list[str]` vira `Session.messages: list[Message]`.

**2. `refactor: handle_input passa a registrar mensagens (user+assistant)`**
A responsabilidade de registrar a conversa sai de `main.py` (que antes fazia
`session.history.append(req.message)` solto, depois de chamar `handle_input`)
e entra em `handle_input`, que agora registra a rodada completa:
```python
def handle_input(session: Session, user_input: str) -> str:
    user_input = user_input.strip()
    reply = _resolve_reply(session, user_input)
    session.messages.append(Message("user", user_input))
    session.messages.append(Message("assistant", reply))
    return reply
```

**3. `feat: adiciona build_payload — monta payload de conversação role/content`**
```python
SYSTEM_PROMPT = "Você é o assistente de atendimento ao cliente."

def build_payload(session: Session) -> list[dict[str, str]]:
    payload = [{"role": "system", "content": SYSTEM_PROMPT}]
    payload.extend({"role": m.role, "content": m.content} for m in session.messages)
    return payload
```
`SYSTEM_PROMPT` é propositalmente genérico — a Aula 2.3 (Persona não é
fantasia) é quem define identidade/escopo de verdade.

**4. `feat: expõe GET /api/chat/{session_id}/payload`**
```python
@app.get("/api/chat/{session_id}/payload", response_model=PayloadResponse)
def chat_payload(session_id: str) -> PayloadResponse:
    session = _sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="session_id não encontrado")
    return PayloadResponse(session_id=session_id, payload=build_payload(session))
```

**5. `feat: painel de visualização do payload na interface`**
Botão "Ver payload" no header; ao ativar, `app.js` busca o endpoint e mostra
o JSON formatado (`JSON.stringify(data.payload, null, 2)`) num `<pre>`,
atualizando a cada mensagem enviada — dá pra ver o payload crescer ao vivo.

**6. `test: cobre build_payload (payload vazio, ordem, papéis, conteúdo)`**
4 testes novos em `tests/test_payload.py`: sessão vazia só tem o `system`;
ordem de papéis (`system, user, assistant, user, assistant`) depois de uma
rodada; conteúdo bate exatamente com o que `handle_input` retornou; todo item
do payload só tem as chaves `role`/`content`.

Suíte final: **12 testes passando** (8 originais das Aulas 1.3/1.6 + 4 novos).

## Payload real de exemplo (rodado durante a implementação)

```json
[
  {"role": "system", "content": "Você é o assistente de atendimento ao cliente."},
  {"role": "user", "content": ""},
  {"role": "assistant", "content": "Boa noite! Bem-vindo ao suporte. Como posso te ajudar hoje?\n\nEscolha uma opção:\n1. Suporte técnico\n2. Questões de faturamento\n3. Informações de conta\n4. Falar com um atendente"},
  {"role": "user", "content": "1"},
  {"role": "assistant", "content": "Você está em Suporte técnico. Descreva o problema em poucas palavras que um atendente vai te responder em instantes."}
]
```

## Validação (real, rodada a cada etapa)

```bash
docker compose build app
docker compose run --rm app python -m pytest -v
```

Validação manual: `docker compose up --build`, abrir `http://localhost:8010`,
clicar "Ver payload", interagir com o menu e conferir que o JSON exibido bate
com o que foi digitado/respondido (confirmado via screenshot durante a
implementação).

## Fluxo git usado

```bash
git checkout m01-a06-end   # não "main" — main tinha commits de docs sem relação com o lab
git tag m02-a01-start
git checkout -b lesson/m02-a01-payload-conversacao
# 6 commits pequenos (acima)
git checkout main
git merge --no-ff lesson/m02-a01-payload-conversacao
git tag m02-a01-end
git push origin main --tags
```

## Como isso conecta os fundamentos (pra narração)

- **Desmistificação da "mágica"** — o chat não "entende a conversa": ele
  recebe uma lista ordenada de mensagens com papel e conteúdo, ponto. É
  literalmente esse payload que qualquer API de LLM consome.
- **Papéis (`system`/`user`/`assistant`)** — introduz o vocabulário que toda
  a Aula 2.x (e o curso inteiro) vai usar dali em diante.
- **Sem antecipar módulos futuros** — `SYSTEM_PROMPT` é um placeholder
  deliberadamente genérico (Persona é 2.3); o payload é montado mas nenhuma
  LLM é chamada (geração real é 2.8); nada de resumo/compactação (2.5).
- **Gancho direto pra 2.8** — quando a primeira chamada generativa existir,
  o payload que ela vai enviar já é exatamente esse que o aluno está vendo
  crescer no painel desde a 2.1.

## Entrega da aula (pra narração)

> Todo chat, por baixo, é uma lista de mensagens com papel e conteúdo — e
> agora dá pra ver essa lista crescendo em tempo real.

O laboratório ganha uma janela pra dentro de si mesmo: o mesmo comportamento
de sempre (menu determinístico), mas agora com o payload de conversação
exposto e visível.
