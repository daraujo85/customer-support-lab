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

## Artefatos prontos pra execução (só falta o áudio pra ancorar as cues)

### `demo.sh` da cena 2 (terminal — Claude scaffold + docker up)

```bash
#!/usr/bin/env bash
set -e
export TERM=xterm-256color DOTNET_NOLOGO=1
GREEN='\033[38;5;113m'; DIM='\033[38;5;245m'; RESET='\033[0m'; BOLD='\033[1m'
prompt(){ printf "${GREEN}${BOLD}➜${RESET}  ${DIM}customer-support-lab${RESET} "; }
run(){ local cmd="$1" c; prompt
  for (( i=0; i<${#cmd}; i++ )); do c="${cmd:$i:1}"; printf '%s' "$c"; sleep 0.0$(( RANDOM % 6 + 4 ))
    if (( RANDOM % 100 < 3 )); then sleep 0.$(( RANDOM % 3 + 2 )); fi; done
  printf '\n'; sleep 0.35; eval "$cmd"; sleep 0.6; }

source /demo/lib/shims.sh
install_shim claude
export CLAUDE_SHIM_MODE=scaffold

clear; sleep 0.6
mkdir -p /tmp/customer-support-lab && cd /tmp/customer-support-lab

run 'claude "crie o baseline do laboratório: FastAPI servindo a página HTML com o fluxo determinístico (saudação por horário, menu fixo, árvore de decisão)"'
sleep 1.0
# docker compose up --build precisa de Docker-in-Docker ou de rodar fora do sandbox
# do terminal-demo (ele já roda DENTRO de um container). Ver nota abaixo.
prompt; sleep 2.0
```

**Nota sobre o `docker compose up --build` dentro do clipe**: o `terminal-demo` já
roda o `demo.sh` DENTRO de um container (`garagem-term-sandbox`) — não tem Docker
aninhado por padrão. Duas opções:
1. Gravar essa parte (`docker compose up --build` + validação no navegador) como
   um clipe SEPARADO, rodado no HOST de verdade (não no sandbox do terminal-demo) —
   mais simples e já validado nesta sessão (funciona, porta 8010).
2. Instalar Docker CLI + socket bind no sandbox (mais complexo, não recomendado só
   pra esta aula).
A opção 1 é a recomendada: dois clipes de terminal (um do shim do Claude, outro do
`docker compose up --build` real no host), cortados juntos na cena 2.

### `actions.json` da cena 3 (navegador — capturar-web)

```json
[
  { "type": "wait", "ms": 1500 },
  { "type": "click", "selector": "#input" },
  { "type": "type", "selector": "#input", "text": "1" },
  { "type": "wait", "ms": 400 },
  { "type": "click", "selector": "button[type=submit]" },
  { "type": "wait", "ms": 1800 }
]
```

Comando (com `docker compose up --build` já rodando em outro terminal, no host):
```bash
node ~/.claude/skills/capturar-web/capweb.js \
  --url http://localhost:8010 --out clip-chat.mp4 \
  --seconds 6 --actions actions.json --width 1280 --height 720
```

### `scene.json` da cena 4a — `app/chat/state.py` (editor-demo)

```json
{
  "title": "app/chat/state.py — customer-support-lab",
  "repo": "customer-support-lab",
  "file": "app/chat/state.py",
  "lang": "python",
  "explorer": ["app/main.py", "app/chat/flow.py", "app/chat/state.py", "Dockerfile"],
  "active": "app/chat/state.py",
  "base": "class ChatState(str, Enum):\n    GREETING = \"greeting\"\n    MAIN_MENU = \"main_menu\"\n    SUPORTE_TECNICO = \"suporte_tecnico\"\n    FINANCEIRO = \"financeiro\"\n    INFORMACOES_CONTA = \"informacoes_conta\"\n    HUMAN_HANDOFF = \"human_handoff\"\n    ENCERRADO = \"encerrado\"\n",
  "typed": "",
  "startDelayMs": 500,
  "holdMs": 4000
}
```

### `scene.json` da cena 4b — `app/chat/flow.py` (editor-demo)

```json
{
  "title": "app/chat/flow.py — customer-support-lab",
  "repo": "customer-support-lab",
  "file": "app/chat/flow.py",
  "lang": "python",
  "explorer": ["app/main.py", "app/chat/flow.py", "app/chat/state.py", "Dockerfile"],
  "active": "app/chat/flow.py",
  "base": "def handle_input(session: Session, user_input: str) -> str:\n    user_input = user_input.strip()\n\n    if session.state == ChatState.GREETING:\n        session.state = ChatState.MAIN_MENU\n        return f\"{greeting()}\\n\\n{menu_text()}\"\n\n    if session.state == ChatState.MAIN_MENU:\n        option = next((o for o in MAIN_MENU if o.key == user_input), None)\n        if option is None:\n            return \"Não entendi. \" + menu_text()\n        session.state = option.next_state\n        return _FIXED_RESPONSES[option.next_state]\n\n    session.state = ChatState.ENCERRADO\n    return \"Obrigado pelo contato! Se precisar de algo mais, é só chamar de novo.\"\n",
  "typed": "",
  "startDelayMs": 500,
  "holdMs": 5000
}
```

Comando pra gerar os dois clipes:
```bash
bash ~/.claude/skills/editor-demo/render.sh scene-state.json clip-state.mp4
bash ~/.claude/skills/editor-demo/render.sh scene-flow.json clip-flow.mp4
```

### Cena 5 — conteúdo dos slides (buildlib, quando o build_esa_m1a3.py existir)

```python
add(<ancora-estado-evento-transicao>, "estado, evento, transição", "", {"graphic": B.g_steps(
    ["Estado", "Evento", "Transição", "Resposta fixa"])})
```

### Falta pra fechar esta aula
- Áudio da narração (segs.json via `segs.py`).
- Decidir se a validação no navegador (cena 3) usa `capturar-web` (screencast real,
  como descrito acima) ou uma sequência de screenshots simples via `sips`/`cap.sh shot`
  — mais barato, menos "vivo".
- Confirmar os anchors reais assim que o texto da narração chegar (os nomes de cena
  acima — "estado, evento, transição" etc. — são placeholders até lá).
