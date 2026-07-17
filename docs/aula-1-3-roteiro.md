# Roteiro técnico — Aula 1.3 "Laboratório: o chatbot determinístico"

Sem áudio ainda (o Diego escreve o TTS no ChatGPT depois). Este documento é o
material de apoio: exatamente o que vai aparecer na tela, na ordem, com os
comandos/arquivos/linhas reais — pra narração casar com a demo sem inventar nada.

## ⚠️ O projeto JÁ EXISTE — a aula não pode narrar "vamos criar agora"

O repo já está criado, commitado (2 commits) e publicado em
`github.com/daraujo85/customer-support-lab` desde ANTES da gravação desta aula. Isso
muda como a Aula 1.3 precisa ser contada:

- **Não roteirizar** frases tipo "agora vamos criar o arquivo `state.py`" ou "vamos
  escrever o menu do zero" como se o código estivesse nascendo ali, ao vivo — isso
  contradiz o histórico real do repo (que o aluno pode abrir e conferir).
- A cena de **terminal** (`git clone` + `docker compose up --build`) está correta
  como está — clonar um repo que já existe é a ação real e coerente.
- A cena de **editor** deve **EXIBIR o código já pronto** (usar o campo `base` do
  `scene.json` do editor-demo, com `typed` vazio ou quase vazio) — **não** usar
  `typed` pra simular que o arquivo está sendo digitado/criado na hora. A narração
  correta é "aqui está o `state.py`" / "repara como o `flow.py` faz essa transição",
  não "vamos digitar isso agora".
- Se quiser um momento de "mão na massa" de verdade nesta aula, a opção coerente é
  mostrar uma pequena alteração INCREMENTAL sobre o que já existe (ex.: adicionar um
  comentário, rodar os testes, ou explorar o código navegando entre abas) — não
  recriar a base do zero.

## Cenas, em ordem

### 1. Herói de abertura
Imagem `art/esa/welcome.png` (mesma do curso), kicker "aula 1.3 · módulo 1", título
"Laboratório: o chatbot determinístico".

### 2. TERMINAL — clonar e subir o projeto (terminal-demo, real)

Comandos, na ordem (todos reais, rodam de verdade num sandbox com Docker):

```bash
git clone https://github.com/daraujo85/customer-support-lab
cd customer-support-lab
docker compose up --build
```

Output esperado: build da imagem (`python:3.12-slim` + pip install fastapi/uvicorn/
pydantic/pytest/httpx — leva uns 15-20s), depois `Uvicorn running on http://0.0.0.0:8000`
dentro do container (mapeado pra **`localhost:8010`** no host — ver `docs/tts-context.md`
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

- Repo: `https://github.com/daraujo85/customer-support-lab` — se a aula pedir pra
  clonar, é essa URL.
- Porta real: **8010** (não 8000).
- O texto do menu e das respostas fixas é EXATAMENTE o que está no código acima —
  se o roteiro parafrasear, a demo ao vivo não vai bater com a legenda/narração.
- A saudação muda com o horário real da máquina no momento da gravação.
- Comando de subir: `docker compose up --build`. Comando de teste (se for mostrar):
  `docker compose run --rm app python -m pytest` (não usar só `pytest`).
