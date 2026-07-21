# Aula 2.8 — Primeira evolução generativa

```text
Branch: lesson/m02-a08-primeira-evolucao-generativa
Base: tag m02-a08-start (a partir da main, no estado de m02-a05-end — as
      Aulas 2.6 "Estado de usuário, sessão e fluxo" e 2.7 "Componentes
      probabilísticos e determinísticos" foram conceituais e não alteraram
      o repositório)
Alteração no laboratório: entrada livre no menu (e nos estados de domínio já
      conhecidos) passa a poder ser resolvida por um componente generativo —
      classificação de intenção, score de confiança e geração de resposta
      por template
Commit: commits pequenos, mergeados --no-ff na main
```

## Ressalva que precisa ser dita com todas as letras

**Nesta aula não existe chamada de LLM, API externa ou custo por token.**

A arquitetura generativa entra agora. A inferência por modelo, não.

`LocalDidacticComponent` é uma implementação REAL do contrato
`GenerativeComponent` — usada durante a execução normal do laboratório, não
um mock de teste — mas é local, determinística e didática: simula a
FRONTEIRA de uma integração probabilística (classificação, score, geração de
resposta) sem aleatoriedade e sempre reproduzível. O score não é uma
probabilidade calibrada de nenhum modelo; é um número calculado por regras.
A resposta não é gerada livremente; é selecionada por template.

Não dizemos "a IA analisou a mensagem". Dizemos "o componente local
classificou a mensagem por regras didáticas".

A primeira inferência real (LLM de verdade) fica para uma aula futura,
explicitamente autorizada.

## Objetivo prático

Até aqui, texto livre no menu principal sempre caía em "Não entendi." — só
opções numéricas exatas avançavam o fluxo. Esta aula introduz um componente
que classifica a intenção por regras/palavras-chave, calcula um score
determinístico e gera uma resposta contextual por template, preservando as
garantias construídas nas aulas anteriores:

- **Opções numéricas continuam determinísticas** — o componente nunca é
  chamado nesse caminho.
- **O código valida toda mudança de estado** — o componente sugere a
  intenção (`Intent`); uma tabela explícita (`INTENT_TO_STATE`) é quem
  decide o estado seguinte.
- **Empate, ausência de evidência (score < 0.70) ou componente desligado
  acionam o mesmo fallback determinístico** que já existia.
- **Handoff humano continua com resposta fixa** — mesmo quando reconhecido
  pelo componente, a resposta proposta é ignorada; usa-se sempre o texto já
  existente.

## O que foi alterado (só isto)

```text
app/chat/generative.py       — NOVO: contrato GenerativeComponent, Intent,
                                ResolutionMode, GeneratedTurn, MIN_ACCEPTED_SCORE
                                (0.70), build_generative_messages(session, input)
app/chat/local_generation.py — NOVO: LocalDidacticComponent — normalização,
                                regras de classificação por frase/palavra-chave,
                                score determinístico, geração por template
app/chat/flow.py             — handle_input ganha `component` opcional; texto
                                livre no menu e nos estados de domínio já
                                conhecidos passa pelo componente antes de
                                decidir a transição; INTENT_TO_STATE explícito
app/chat/summary.py          — update_summary ganha `resolution_mode` e
                                `resolved_state`; novos casos de transição
                                (MAIN_MENU->ENCERRADO via componente local,
                                domínio->HUMAN_HANDOFF via fallback)
app/main.py                  — GENERATION_MODE (local_didactic | disabled)
                                escolhe a implementação injetada no boot
docker-compose.yml            — GENERATION_MODE: ${GENERATION_MODE:-local_didactic}
tests/test_local_generation.py — NOVO: 8 testes (normalização, classificação
                                por domínio, handoff, UNKNOWN por ausência de
                                evidência, UNKNOWN por empate, expected_intent
                                sem reclassificar)
tests/test_generative_flow.py  — NOVO: 8 testes (saudação/opção numérica não
                                chamam o componente, texto livre reconhecido
                                encerra o fluxo e registra resumo, UNKNOWN usa
                                fallback, handoff usa resposta fixa, componente
                                desligado/indisponível aciona fallback)
```

Alterado só em comentários/documentação (a Aula 2.8 deixou de ser descrita
como "primeira chamada de LLM real"): `app/chat/state.py`,
`app/chat/payload.py`, `README.md`, `docs/tts-context.md`,
`docs/workflow-git.md`.

Não alterado: `pyproject.toml`, `Dockerfile`, `app/chat/persona.py`,
`app/static/*`. Nenhuma dependência nova.

## Validação manual

```bash
# Estado anterior — texto livre ainda não funciona
git switch --detach m02-a08-start
docker compose run --rm app python -m pytest -v   # 24 passed

# Estado final — componente local ativo
git switch --detach m02-a08-end
docker compose up --build
# http://localhost:8010
# "Meu computador não liga."        -> classificação + resposta contextual
# "Preciso de ajuda."                -> fallback determinístico (UNKNOWN)
# "Quero falar com um atendente."    -> handoff com resposta fixa

# Fallback com componente desligado — prova que é capacidade adicional
GENERATION_MODE=disabled docker compose up --build
```

## A frase central da aula

> O componente local simula a fronteira probabilística. O código continua
> responsável pelas decisões reais.
