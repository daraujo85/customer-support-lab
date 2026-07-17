# Arquitetura

Laboratório evolutivo do curso **Engenharia de Software na Era dos Agentes**. Domínio
fictício (atendimento ao cliente genérico) — sem dado real de clientes ou negócio.

## Estado atual (Aula 1.3)

Um único container Python com FastAPI:

- `app/main.py` serve a página estática (`app/static/`) e expõe `POST /api/chat`.
- `app/chat/state.py` define os estados da máquina (`ChatState`) e a sessão.
- `app/chat/flow.py` implementa a árvore de decisão: saudação por horário, menu
  fixo numerado, transição de estado por opção escolhida, resposta fixa e
  encerramento. **Zero geração de linguagem** — cada resposta é texto fixo
  escolhido por regra explícita.

Sessão fica em memória do processo (`_sessions` em `main.py`) — não sobrevive a um
restart do container. A separação entre estado de usuário, de sessão e de execução
vem na Aula 2.6.

## Arquitetura aspiracional (evolução planejada)

Este container e este fluxo são o ponto de partida, não o produto final. Ao longo do
curso, o mesmo domínio evolui para:

1. **Generativo** (Módulo 2) — entrada livre + classificação de intenção, com o menu
   determinístico preservado como fallback.
2. **Contextual** (Módulo 3) — Specs versionadas via `tlc-spec-driven`, contexto em
   camadas, prompts como artefato.
3. **Com ferramentas** (Módulo 4-5) — agente declarativo, function calling, RTK,
   Context7, Playwright.
4. **Multimodal** (Módulo 6) — áudio, imagem, vídeo; canal HTML + WhatsApp sobre o
   mesmo motor.
5. **Ecossistema de agentes especializados** (Módulo 4, 6) — triagem, financeiro,
   suporte, handoff humano.

PostgreSQL, Redis e demais serviços entram **somente quando uma dor concreta da aula
justificar** — nunca antes. Ver `docs/course-roadmap.md`.
