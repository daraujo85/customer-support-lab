# Roadmap do laboratório por módulo

Referência rápida de qual aula introduz qual peça — evita adicionar complexidade
antes da dor que a justifica (ver `docs/architecture.md`).

| Módulo | O que entra no laboratório |
|---|---|
| 1 — O Engenheiro na Era dos Agentes | Chatbot determinístico: HTML, saudação por horário, menu fixo, árvore de decisão (Aula 1.3). |
| 2 — Anatomia de uma Conversa com um LLM | Entrada livre, roles, janela de contexto, resumo, primeira evolução generativa (Aula 2.8). |
| 3 — SDD e Engenharia de Contexto | Specs via `tlc-spec-driven`, contexto em camadas, prompts versionados. |
| 4 — Runtime, Grafos e Orquestração | Agente declarativo (JSON), grafo de conversa, múltiplos agentes, controle de loop. |
| 5 — Skills, Tools, MCPs | Function calling, tools (banco read-only, RTK, Context7, Playwright, FFmpeg). |
| 6 — Do Chatbot ao Agente Multimodal | Small talk, guard rails, FAQ/RAG, memória, áudio, imagem, vídeo, canal WhatsApp. |
| 7 — Arquitetura Agnóstica | Adapter de provider, troca prática entre dois providers. |
| 9 — Qualidade, Feedback e Observabilidade | Testes gerados por agente, Playwright E2E, tracing, métricas. |
| 10 — Memória, Grafos, SLMs | AgentMemory, contexto em grafo, Graphify, SLM. |
| 11 — Operação e Paralelo | Pipeline/deploy, CloudWatch, paralelismo com Git Worktree. |

PostgreSQL, Redis, Elasticsearch/pgvector e qualquer outro serviço só entram no
`docker-compose.yml` no módulo que efetivamente precisar deles.
