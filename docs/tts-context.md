# Contexto pro roteiro de TTS — o que foi implementado de verdade

Cole isto junto do prompt de narração. Ele resume TUDO que foi criado no projeto
`customer-support-lab`, incluindo os pontos onde a implementação real diverge (ou
precisa ser mais específica) do que foi combinado no chat original.

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
    test_chat_flow.py        # 4 testes, todos passando
  docs/
    architecture.md
    course-roadmap.md
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

## Identidade dos commits

Commits vão com `Diego Araújo <jcresgate@gmail.com>` (identidade pessoal) — se a
narração mostrar um `git log` ou `git blame`, é esse nome/e-mail que aparece, não o
do Prata Digital.
