# Contexto pro roteiro de TTS — o que foi implementado de verdade

Cole isto junto do prompt de narração. Ele resume TUDO que foi criado no projeto
`customer-support-lab`, incluindo os pontos onde a implementação real diverge (ou
precisa ser mais específica) do que foi combinado no chat original.

## ⚠️ Regra geral: o projeto JÁ EXISTE — não narrar como "criando agora"

O repo já está criado, testado e publicado ANTES de qualquer aula ser gravada. Isso
vale pra `customer-support-lab` inteiro, em qualquer módulo/aula futura, não só a
1.3:

- A demo em vídeo **finge** estar trabalhando ao vivo no projeto (pra fins
  didáticos/narrativos), mas na real está **mostrando/revisando o que já existe**.
- **Nunca** roteirizar "vamos criar o arquivo X agora" ou "vamos escrever isso do
  zero" quando o arquivo já está commitado no repo — o aluno pode conferir o
  histórico do GitHub e a contradição fica visível.
- Cena de **editor** (Monaco): usar sempre `base` (conteúdo já pronto, exibido
  instantaneamente) para código que já existe no repo. Só usar `typed` (animação de
  digitação) para uma alteração NOVA e INCREMENTAL que a aula está genuinamente
  introduzindo naquele momento (ex.: um módulo futuro adicionando uma função nova
  em cima do que já existe).
- Cena de **terminal**: comandos tipo `git clone` / `docker compose up` continuam
  corretos (é a ação real de baixar/rodar um projeto existente) — o problema é só
  fingir que o CONTEÚDO nasceu ali.

## Repositório

- **URL pública**: `https://github.com/daraujo85/customer-support-lab`
- **Pasta local**: `~/Desktop/gc/customer-support-lab` (Área de Trabalho — NÃO cite
  "Documents" ou "projects" na narração, o repo real do Diego não fica lá).

## ⚠️ Porta — DIVERGE do padrão óbvio

O combinado foi "sobe com `docker compose up --build`, abre o navegador, valida o
chatbot" — sem especificar porta. **A porta do HOST é 8010, não 8000.**

- Motivo: a porta 8000 já está ocupada na máquina de gravação por outro serviço
  (`sessionflow-api`, um produto à parte do Diego, sem relação com o curso).
- Dentro do container o Uvicorn roda em 8000 normalmente; o mapeamento no
  `docker-compose.yml` é `"8010:8000"`.
- **Se o roteiro disser "abra `localhost:8000`", está ERRADO.** O correto é:
  **`http://localhost:8010`**.

## Comandos exatos (usar literalmente na narração/legenda)

```bash
docker compose up --build
```
→ abre `http://localhost:8010` no navegador.

```bash
docker compose run --rm app python -m pytest
```
→ roda os testes. **Atenção**: `pytest` sozinho (sem o `python -m`) FALHA com
`ModuleNotFoundError: No module named 'app'` (problema de `sys.path` dentro do
container). Se a aula for mostrar rodando os testes, o comando tem que ser esse,
com `python -m` na frente — não simplifique pra só `pytest`.

## Estrutura de arquivos criada (bate com o combinado)

```
customer-support-lab/
  app/
    __init__.py
    main.py                # FastAPI: serve a página + POST /api/chat
    chat/
      __init__.py
      flow.py               # árvore de decisão determinística
      state.py              # ChatState (enum), MenuOption, Session
    static/
      index.html
      app.js
      styles.css
  tests/
    test_chat_flow.py        # 8 testes, todos passando (4 da Aula 1.3 + 4 da Aula 1.6)
    test_payload.py          # 4 testes da Aula 2.1 — 12 testes no total
  docs/
    architecture.md
    course-roadmap.md
    workflow-git.md           # fluxo de branch+tag por aula + tabela de quais aulas alteram o repo
    aula-1-3-roteiro.md       # registro do que foi de fato gravado, aula a aula
    aula-1-4-roteiro.md
    aula-1-5-roteiro.md
    aula-1-6-roteiro.md
    tts-context.md            # este arquivo
  specs/                      # vazio (.gitkeep) — passa a receber Specs no Módulo 3
  skills/                     # vazio (.gitkeep)
  Dockerfile
  docker-compose.yml
  pyproject.toml
  README.md
  .gitignore
```

## O que o chatbot determinístico (Aula 1.3) faz de verdade

- **Saudação por horário real do sistema** (`datetime.now().hour`): "Bom dia" (antes
  das 12h), "Boa tarde" (12h–18h), "Boa noite" (depois das 18h). Se a aula for
  gravada de manhã, a demo vai mostrar "Bom dia" — não force um horário específico
  no roteiro sem checar quando a gravação vai rolar.
- **Menu fixo, numerado 1 a 4** (texto exato, se for citar na narração):
  1. Suporte técnico
  2. Questões de faturamento
  3. Informações de conta
  4. Falar com um atendente
- Cada opção leva a um **estado fixo** com resposta fixa (sem geração de linguagem):
  `SUPORTE_TECNICO`, `FINANCEIRO`, `INFORMACOES_CONTA`, `HUMAN_HANDOFF`.
- Entrada não reconhecida no menu **não avança o estado** — repete o menu com "Não
  entendi.".
- Sessão fica em **memória do processo** (dicionário Python), não persiste se o
  container reiniciar — isso é proposital nesta aula; a Aula 2.6 é quem separa
  estado de usuário/sessão/execução.
- **Domínio 100% fictício**: atendimento ao cliente genérico. Nenhum dado de
  cliente ou negócio real.
- **Desde a Aula 1.6**: a resolução da opção do menu não é mais uma busca
  inline dentro de `handle_input` — foi extraída pra uma função de domínio
  explícita `resolve_menu_option(user_input: str) -> MenuOption | None` em
  `app/chat/flow.py`. Comportamento externo idêntico; só a estrutura interna
  mudou (regra nomeada e testável isoladamente). Se o roteiro citar código de
  `flow.py`, usar essa versão — não a busca inline antiga.

## ⚠️ Quais aulas alteram o repositório (não assumir pelo número da aula)

Nem toda aula com laboratório na tela **altera** o repositório. Regra e
tabela completa (todos os módulos) em `docs/workflow-git.md` — **consultar
esse arquivo antes de narrar qualquer branch/commit**, nunca assumir. Estado
atual do Módulo 1: 1.1/1.2 conceituais (sem lab), 1.3 cria o baseline
(commitado direto na `main`, antes do fluxo de branch existir), 1.4 e 1.5 são
só leitura/análise (Claude Code não escreve nada, sem branch), 1.6 tem
evolução real (`lesson/m01-a06-fundamentos-engenharia`, mergeada na `main`),
1.7 é demonstração da esteira já existente (histórico real + docs reais +
Claude Code em modo análise via shim — árvore começa e termina limpa, sem
branch/commit novo), 1.8 fecha o módulo com prova/reflexão (10 situações de
julgamento + Claude Code em modo análise preparando avaliação/delegação/
evolução desnecessária — também sem branch/commit novo).

## Dependências e versões (se o roteiro for citar tecnologia por nome)

- Python **3.12** (imagem `python:3.12-slim` no Dockerfile; `pyproject.toml` pede
  `>=3.11`).
- FastAPI `>=0.115`, Uvicorn `[standard] >=0.32`, Pydantic `>=2.9`.
- Pytest `>=8.3` + httpx `>=0.27` (só usado em testes futuros com `TestClient`; os 4
  testes atuais testam a função `handle_input` direto, sem subir servidor).

## O que ainda NÃO existe (não citar como pronto)

- PostgreSQL, Redis, Elasticsearch/pgvector — **não fazem parte do compose ainda**.
  Só entram no módulo do curso que efetivamente precisar (ver
  `docs/course-roadmap.md` no repo para o mapeamento módulo → peça nova).
- Nenhuma chamada de LLM/IA existe no código ainda — a primeira entra na Aula 2.8.
- `specs/` e `skills/` estão vazios — populam a partir do Módulo 3 (skill
  `tlc-spec-driven`).

## Aula 2.1 — "O que existe por trás de um chat" (payload de conversação)

Roteiro completo em `docs/aula-2-1-roteiro.md` — resumo aqui pro TTS:

- **Branch**: `lesson/m02-a01-payload-conversacao`, derivada da tag
  `m01-a06-end` (não da `main` — a `main` tinha commits de docs/fotonovela à
  frente, sem relação com o laboratório).
- **Tags**: `m02-a01-start` / `m02-a01-end`. 6 commits pequenos, merge
  `--no-ff` na `main`.
- **Arquivos alterados**: `app/chat/state.py` (nova `Message`,
  `Session.messages` no lugar de `Session.history`), `app/chat/flow.py`
  (`handle_input` agora registra cada rodada user+assistant),
  `app/chat/payload.py` (**novo** — `build_payload(session)`), `app/main.py`
  (**novo** endpoint `GET /api/chat/{session_id}/payload`),
  `app/static/index.html` + `app.js` + `styles.css` (painel "Ver payload" na
  interface), `tests/test_payload.py` (**novo**, 4 testes).
- **Nenhuma chamada de LLM existe ainda** — esta aula só monta e EXPÕE o
  payload no formato role/content; a primeira geração real é a Aula 2.8.
- **Comportamento final**: ao clicar "Ver payload" no header do widget, um
  painel `<pre>` mostra o JSON do payload da sessão atual, atualizando a cada
  mensagem enviada. Formato exato (`system` sempre primeiro, propositalmente
  genérico — Persona de verdade é Aula 2.3):
  ```json
  [
    {"role": "system", "content": "Você é o assistente de atendimento ao cliente."},
    {"role": "user", "content": ""},
    {"role": "assistant", "content": "Boa noite! Bem-vindo ao suporte..."},
    {"role": "user", "content": "1"},
    {"role": "assistant", "content": "Você está em Suporte técnico..."}
  ]
  ```
- **Comando de teste** (mesmo padrão de sempre):
  ```bash
  docker compose build app
  docker compose run --rm app python -m pytest -v
  ```
  → 12 testes passando (8 antigos + 4 novos de `test_payload.py`).
- **Endpoint novo pra citar/mostrar na narração**: `GET
  /api/chat/{session_id}/payload` → `{"session_id": "...", "payload": [...]}`
  (404 se `session_id` não existir).

## Identidade dos commits

Commits vão com `Diego Araújo <jcresgate@gmail.com>` (identidade pessoal) — se a
narração mostrar um `git log` ou `git blame`, é esse nome/e-mail que aparece, não o
do Prata Digital.
