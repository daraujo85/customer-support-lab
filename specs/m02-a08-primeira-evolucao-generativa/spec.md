# Spec — Primeira evolução generativa (retroativa)

> **Status: `already_implemented` (retroativa).** Esta especificação foi
> escrita DEPOIS da implementação (Aula 2.8, branch
> `lesson/m02-a08-primeira-evolucao-generativa`, tags `m02-a08-start` →
> `m02-a08-end`, já mergeada em `main`). O objetivo não é autorizar uma
> execução nova — é reconstruir o contrato que deveria ter existido antes
> dela, usando código, testes e histórico de commit como evidência.

## Contexto histórico

Até o checkpoint `m02-a08-start`, o laboratório resolvia texto livre no
menu principal apenas com a resposta fixa "Não entendi. Escolha uma
opção:" — só as opções numéricas (`1`–`4`) avançavam o atendimento. As
Aulas 2.1–2.7 já tinham construído payload de conversação, persona,
resumo estruturado e a distinção conceitual entre componente
determinístico e componente probabilístico, mas nenhum componente
probabilístico de verdade existia ainda.

## Problema resolvido

Um usuário que escrevesse a intenção em linguagem natural (ex. "meu
computador não liga") em vez de escolher uma opção numérica não conseguia
avançar o atendimento — o sistema sempre devolvia o menu, mesmo quando a
intenção era clara para um humano.

## Objetivo

Introduzir uma fronteira generativa que classifique texto livre e gere uma
resposta contextual, **sem** chamar nenhuma LLM, API externa ou serviço
pago — para fins didáticos, o "componente probabilístico" é simulado por
um componente local, determinístico e reproduzível
(`LocalDidacticComponent`, em `app/chat/local_generation.py`), atrás de um
contrato substituível (`GenerativeComponent`, em `app/chat/generative.py`)
que permitiria, no futuro, trocar essa implementação por um provider real
sem alterar a máquina de estados, o resumo ou os testes de domínio.

## Escopo

**Dentro do escopo:**
- Classificação de texto livre no menu principal (suporte técnico,
  financeiro, informações de conta, atendimento humano, ou `UNKNOWN`).
- Geração de resposta contextual por template para intenções reconhecidas.
- Validação do score pelo código antes de qualquer mudança de estado.
- Fallback determinístico para score insuficiente, empate ou componente
  indisponível/desligado.
- Registro no resumo estruturado de como cada turno foi resolvido
  (`resolution_mode`: `deterministic` | `local_didactic` | `fallback`).

**Fora do escopo** (explicitamente, ver `docs/aula-2-8-roteiro.md`):
- Qualquer integração real de LLM, API externa, modelo local ou serviço
  pago (`Groq`, `OpenAI`, `Anthropic`, `Ollama`, chamada HTTP de rede).
- Aleatoriedade artificial para simular incerteza.
- Mudança na interface (`app/static/*`) ou no contrato de payload das
  aulas anteriores.

## Requisitos funcionais

1. Opções numéricas (`1`–`4`) continuam determinísticas — o componente
   generativo nunca é chamado nesse caminho.
2. Texto livre no menu principal é classificado por
   `LocalDidacticComponent.generate()`, que devolve intenção, score e
   termos encontrados.
3. Um score `>= MIN_ACCEPTED_SCORE` (0.70) e uma intenção não-`UNKNOWN`
   levam à transição `MAIN_MENU → ENCERRADO` com resposta gerada por
   template (exceto handoff, ver item 5).
4. Score insuficiente, `UNKNOWN` ou empate entre intenções mantêm o estado
   em `MAIN_MENU` e usam o fallback determinístico do menu — nenhuma
   intenção é inventada, nenhum fato/decisão é registrado no resumo.
5. Intenção de encaminhamento humano (`HUMAN_HANDOFF`) tem prioridade,
   mas a resposta do componente é **ignorada** — o fluxo usa
   obrigatoriamente a mensagem fixa de encaminhamento humano já existente.
6. Num estado de domínio já conhecido (usuário já escolheu uma opção
   numérica), o componente recebe `expected_intent` e **não reclassifica**
   — só seleciona o template de resposta.
7. Componente indisponível (`GenerativeComponentError`) ou desligado
   (`component=None`, equivalente a `GENERATION_MODE=disabled`) aciona o
   mesmo fallback determinístico de encaminhamento humano.
8. O resumo estruturado (`chat.summary`) registra o modo de resolução de
   cada turno, preservando as regras de fatos/decisões/pendências já
   estabelecidas na Aula 2.5.

## Comportamentos determinísticos preservados

- `resolve_menu_option` e a árvore de transição de `flow._resolve_reply`
  continuam inalterados para entrada numérica.
- `RECENT_MESSAGE_LIMIT` (payload compacto) e a persona (`chat.persona`)
  continuam funcionando sem qualquer dependência do componente novo.
- O histórico bruto (`session.messages`) nunca é truncado — só o que é
  ENVIADO no payload é compactado (contrato herdado da Aula 2.5).

## Score — o que ele é e o que não é

- Calculado por regras locais (frase forte = 1.0; 3+ palavras-chave =
  0.90; 2 = 0.80; 1 = 0.70; nenhuma = 0.0) em
  `local_generation.classify_intent`.
- **Não representa uma probabilidade calibrada de nenhum modelo
  estatístico** — é apenas um número determinístico e reproduzível.

## Ausência de LLM, API externa e custo

Nenhum `import` de SDK de IA, cliente HTTP externo ou variável de
ambiente de credencial existe em `app/chat/local_generation.py` ou
`app/chat/generative.py`. `pyproject.toml` não lista dependência de
provider de IA. `GENERATION_MODE=local_didactic` é o único modo com
implementação real; `disabled` desliga a camada por completo.

## Limitações conhecidas

- A lista de frases/palavras-chave por intenção é pequena e didática —
  não é um sistema de linguagem natural completo (limitação proposital,
  não um bug a corrigir).
- O score não se recalibra com uso; é uma tabela fixa de regras.

## Itens fora do escopo desta Spec

- Substituir `LocalDidacticComponent` por um provider real (ver seção
  "Como substituir no futuro" em `docs/aula-2-8-roteiro.md`) — decisão
  explícita futura do Diego, não desta aula.
- Refinar a própria qualidade desta Spec (critérios de aceite mais
  granulares, rastreabilidade requisito↔teste explícita) — fica para a
  Aula 3.4, que analisa a anatomia desta primeira Spec.

## Evidências já existentes

40 testes passando (24 anteriores + 16 novos), sem acesso a rede, sem
chave, sem custo:

- `tests/test_local_generation.py` (8 testes): normalização
  (`test_normalize_removes_case_and_accents`), classificação por domínio
  (`test_classifies_technical_message`, `test_classifies_billing_message`,
  `test_classifies_account_message`), handoff
  (`test_identifies_human_handoff_request`), ausência de evidência
  (`test_returns_unknown_without_evidence`), empate
  (`test_returns_unknown_on_tie_between_intents`), intenção esperada sem
  reclassificar (`test_expected_intent_skips_reclassification`).
- `tests/test_generative_flow.py` (8 testes): saudação e opção numérica
  não chamam o componente (`test_greeting_does_not_call_component`,
  `test_numeric_option_does_not_call_component`), texto livre reconhecido
  encerra o fluxo e atualiza o resumo
  (`test_recognized_free_text_generates_reply_and_ends_flow`,
  `test_recognized_free_text_records_fact_decision_and_preserves_history`),
  UNKNOWN e fallback (`test_unknown_intent_keeps_menu_state_and_uses_fallback`),
  handoff (`test_handoff_intent_uses_fixed_response`), componente
  desligado (`test_disabled_component_in_menu_uses_fallback`) e
  componente indisponível num domínio já conhecido
  (`test_unavailable_component_in_domain_triggers_handoff_and_updates_summary`).

## Tags da implementação original

`m02-a08-start` → `m02-a08-end`, branch
`lesson/m02-a08-primeira-evolucao-generativa`, já mergeada em `main`
(merge commit da Aula 2.8).
