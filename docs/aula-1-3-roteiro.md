# Roteiro técnico — Aula 1.3 "Laboratório: o chatbot determinístico"

Sem áudio ainda (o Diego escreve o TTS no ChatGPT depois). Este documento é o
material de apoio: exatamente o que vai aparecer na tela, na ordem, com os
comandos/arquivos/linhas reais — pra narração casar com a demo sem inventar nada.

## ⚠️ O projeto JÁ EXISTE — a aula não pode narrar "vamos criar agora"

O repo já está criado, commitado e publicado em
`github.com/daraujo85/customer-support-lab` desde ANTES da gravação desta aula. Isso
muda como a Aula 1.3 precisa ser contada — mas a aula FALA de pedir pro Claude criar
o projeto, então resolvemos assim:

- A cena de **terminal** mostra `claude "<prompt>"` criando o baseline — mas é um
  **shim fake e determinístico** (`CLAUDE_SHIM_MODE=scaffold` no `terminal-demo`,
  ver `garagem-claude-shim-scaffold` na memória), não o Claude Code de verdade.
  Motivo: a conta configurada na máquina de gravação é do Prata Digital (trabalho),
  não pode gerar conteúdo do curso pessoal; e o resultado precisa bater EXATAMENTE
  com o repo já commitado (aulas seguintes citam nome de arquivo/texto exato). O
  shim escreve os arquivos REAIS (idênticos ao repo) com a mesma cara de tool-call
  do Claude Code (`⏺ Write(arquivo)` / `⎿ Wrote N lines`) — visualmente convincente,
  testado ponta a ponta.
- A narração PODE dizer "peça pro Claude criar o baseline" — é literalmente o que a
  tela mostra (só que por trás é o shim, não a API real). Vale fechar mencionando
  que o resultado já está publicado no GitHub pra quem quiser acompanhar/clonar (o
  shim já imprime essa linha no final).
- A cena de **editor**, mais adiante, deve **EXIBIR o código já pronto** (campo
  `base` do `scene.json`, com `typed` vazio) — não digitar de novo o que o terminal
  acabou de "criar". A narração aqui é "repara como o `state.py` ficou" / "o
  `flow.py` faz essa transição assim", não "vamos digitar isso agora".

## Cenas, em ordem

### 1. Herói de abertura
Imagem `art/esa/welcome.png` (mesma do curso), kicker "aula 1.3 · módulo 1", título
"Laboratório: o chatbot determinístico".

### 2. TERMINAL — Claude Code cria o baseline (terminal-demo, shim scaffold)

```bash
claude "crie o baseline do laboratório: FastAPI servindo a página HTML com o fluxo
determinístico (saudação por horário, menu fixo, árvore de decisão)"
```

Com `install_shim claude` + `export CLAUDE_SHIM_MODE=scaffold` no `demo.sh` (ver
memória `garagem-claude-shim-scaffold`). Output: sequência de `⏺ Write(arquivo)` /
`⎿ Wrote N lines` pros 15 arquivos reais do projeto (pyproject.toml, .gitignore,
app/chat/state.py, app/chat/flow.py, app/main.py, app/static/*, tests/test_chat_flow.py,
Dockerfile, docker-compose.yml, docs/architecture.md, docs/course-roadmap.md,
README.md — os dois `__init__.py` vazios são criados em silêncio), terminando com:

```
⏺ Baseline criado. Suba com docker compose up --build e abra
  http://localhost:8010 pra validar.
  Já está publicado no GitHub pra acompanhar: github.com/daraujo85/customer-support-lab
```

Na sequência, o terminal roda `docker compose up --build` de verdade (isso sim é
real, sem shim — o sandbox tem Docker/Python de verdade). Output esperado: build da
imagem (`python:3.12-slim` + pip install fastapi/uvicorn/pydantic/pytest/httpx —
leva uns 15-20s), depois `Uvicorn running on http://0.0.0.0:8000` dentro do
container (mapeado pra **`localhost:8010`** no host — ver `docs/tts-context.md`
sobre por que não é 8000).

### 3. NAVEGADOR — validar o chatbot rodando (captura real de tela/browser)

Abrir `http://localhost:8010`. A viewport mostra o widget de chat (dark, tema
Garagem) já com a saudação disparada automaticamente ao carregar (o `app.js` chama
`send("")` no load). Depois **digitar `1`** no campo e mandar, pra mostrar uma
transição de estado ao vivo (`Suporte técnico`).

Sequência exata de mensagens que vão aparecer na tela (bate com o código real):

1. Bot (automático, ao abrir): `"Bom dia! Bem-vindo ao suporte. Como posso te ajudar hoje?"` seguido do menu:
   ```
   Escolha uma opção:
   1. Suporte técnico
   2. Questões de faturamento
   3. Informações de conta
   4. Falar com um atendente
   ```
   (a saudação muda pra "Boa tarde"/"Boa noite" conforme o horário real de quando
   gravar — ver `docs/tts-context.md`.)
2. Usuário digita `1` e envia.
3. Bot responde: `"Você está em Suporte técnico. Descreva o problema em poucas palavras que um atendente vai te responder em instantes."`

### 4. EDITOR (editor-demo, Monaco real) — mostrar a árvore de decisão

**Exibir como código já pronto** (`base`, sem animação de digitação — ver aviso no
topo do documento). Dois arquivos, nessa ordem (explorer mostrando os 4 arquivos do
`app/`):

**a) `app/chat/state.py`** — mostrar o enum inteiro (isso é o "estado" da máquina de
estados citada na narração):
```python
class ChatState(str, Enum):
    GREETING = "greeting"
    MAIN_MENU = "main_menu"
    SUPORTE_TECNICO = "suporte_tecnico"
    FINANCEIRO = "financeiro"
    INFORMACOES_CONTA = "informacoes_conta"
    HUMAN_HANDOFF = "human_handoff"
    ENCERRADO = "encerrado"
```

**b) `app/chat/flow.py`** — a função `handle_input` (é o "evento → transição" da
narração — recebe o estado atual + a entrada do usuário, devolve a resposta e o
próximo estado):
```python
def handle_input(session: Session, user_input: str) -> str:
    user_input = user_input.strip()

    if session.state == ChatState.GREETING:
        session.state = ChatState.MAIN_MENU
        return f"{greeting()}\n\n{menu_text()}"

    if session.state == ChatState.MAIN_MENU:
        option = next((o for o in MAIN_MENU if o.key == user_input), None)
        if option is None:
            return "Não entendi. " + menu_text()
        session.state = option.next_state
        return _FIXED_RESPONSES[option.next_state]

    session.state = ChatState.ENCERRADO
    return "Obrigado pelo contato! Se precisar de algo mais, é só chamar de novo."
```

Vale citar na narração: **zero geração de linguagem** — toda resposta é texto fixo
escolhido por regra explícita (`_FIXED_RESPONSES`), sem chamar nenhuma IA.

### 5. Slides — recapitular o conceito

Cards ou steps: `Estado` (onde a conversa está) → `Evento` (entrada do usuário) →
`Transição` (regra que decide o próximo estado) → `Resposta fixa`. Reforçar a frase
da ementa: "o determinístico não vai ser descartado quando o generativo entrar" —
esse MESMO `MAIN_MENU`/`ChatState` continua existindo como fallback na Aula 2.8.

### 6. Fechamento
Imagem `art/esa/closing.png`, "Próxima aula: do codador ao orquestrador".

## Coisas que a narração PRECISA saber pra não errar

- Repo: `https://github.com/daraujo85/customer-support-lab` — é a URL que o shim
  cita no final; se a aula quiser reforçar "clone e acompanhe", é essa.
- A cena de "Claude criando o projeto" usa o SHIM (fake, determinístico), não o
  Claude Code real — ver aviso no topo do documento.
- Porta real: **8010** (não 8000).
- O texto do menu e das respostas fixas é EXATAMENTE o que está no código acima —
  se o roteiro parafrasear, a demo ao vivo não vai bater com a legenda/narração.
- A saudação muda com o horário real da máquina no momento da gravação.
- Comando de subir: `docker compose up --build`. Comando de teste (se for mostrar):
  `docker compose run --rm app python -m pytest` (não usar só `pytest`).
