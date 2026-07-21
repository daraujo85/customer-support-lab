# Spec — Primeira evolução generativa (retroativa)

> **Status: `already_implemented` (retroativa).** Esta especificação foi
> escrita DEPOIS da implementação (Aula 2.8, branch
> `lesson/m02-a08-primeira-evolucao-generativa`, tags `m02-a08-start` →
> `m02-a08-end`, já mergeada em `main`). O objetivo não é autorizar uma
> execução nova — é reconstruir o contrato que deveria ter existido antes
> dela, usando código, testes e histórico de commit como evidência.
>
> **Revisão (Aula 3.4, branch `lesson/m03-a04-refinamento-spec`, tags
> `m03-a04-start` → `m03-a04-end`):** a primeira versão (3.3) já tinha
> contexto, escopo, requisitos e evidências, mas critérios de aceite
> estavam misturados com narrativa de implementação e a ligação entre
> requisito e teste era só implícita (citação em texto corrido). Esta
> revisão reorganiza o mesmo conteúdo em critérios de aceite numerados,
> observáveis e binários, com uma matriz de rastreabilidade explícita.
> **Nenhum arquivo de `app/` ou `tests/` muda — só este documento.**

## Contexto e problema

Até o checkpoint `m02-a08-start`, o laboratório resolvia texto livre no
menu principal apenas com a resposta fixa "Não entendi. Escolha uma
opção:" — só as opções numéricas (`1`–`4`) avançavam o atendimento. As
Aulas 2.1–2.7 já tinham construído payload de conversação, persona,
resumo estruturado e a distinção conceitual entre componente
determinístico e componente probabilístico, mas nenhum componente
probabilístico de verdade existia ainda. Um usuário que escrevesse a
intenção em linguagem natural (ex. "meu computador não liga") em vez de
escolher uma opção numérica não conseguia avançar o atendimento — o
sistema sempre devolvia o menu, mesmo quando a intenção era clara para um
humano.

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
- Substituir `LocalDidacticComponent` por um provider real (ver seção
  "Como substituir no futuro" em `docs/aula-2-8-roteiro.md`) — decisão
  explícita futura do Diego, não desta Spec.
- Recalibração do score com uso real — continua sendo uma tabela fixa de
  regras (ver "Riscos e limitações").

## Requisitos

1. Opções numéricas (`1`–`4`) continuam determinísticas — o componente
   generativo nunca é chamado nesse caminho.
2. Texto livre no menu principal é classificado por
   `LocalDidacticComponent.generate()`, que devolve intenção, score e
   termos encontrados.
3. Um score `>= MIN_ACCEPTED_SCORE` (0.70) e uma intenção não-`UNKNOWN`
   levam à transição `MAIN_MENU → ENCERRADO` com resposta gerada por
   template (exceto handoff, ver requisito 5).
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
   cada turno (`resolution_mode`), preservando as regras de
   fatos/decisões/pendências já estabelecidas na Aula 2.5.

## Critérios de aceite por cenário

Cada critério é observável (dá pra checar no resultado, sem olhar
implementação) e binário (passa ou não passa) — liga-se ao requisito
correspondente e à evidência concreta na seção "Evidências".

- **AC-01** — Entrada é opção numérica (`1`–`4`) ou saudação →
  `LocalDidacticComponent.generate()` nunca é chamado; fluxo resolve só
  por `resolve_menu_option`/`flow._resolve_reply`. *(Requisito 1)*
- **AC-02** — Entrada é texto livre, componente devolve intenção conhecida
  (≠ `UNKNOWN`, ≠ `HUMAN_HANDOFF`) com score `>= 0.70` → estado final é
  `ENCERRADO`, resposta vem de template, resumo ganha fato + decisão.
  *(Requisitos 2, 3, 8)*
- **AC-03** — Score `< 0.70` OU empate entre duas intenções → estado
  permanece `MAIN_MENU`, resposta é o fallback fixo do menu, nenhum
  fato/decisão novo é registrado. *(Requisito 4)*
- **AC-04** — Intenção classificada é `HUMAN_HANDOFF` (mesmo com score
  alto) → resposta é sempre a mensagem fixa de encaminhamento humano;
  texto que o componente teria gerado é descartado. *(Requisito 5)*
- **AC-05** — Usuário já está num domínio conhecido (`expected_intent`
  setado, ex. já escolheu opção numérica) → componente recebe
  `expected_intent` e não reexecuta a classificação; só escolhe o
  template de resposta daquele domínio. *(Requisito 6)*
- **AC-06** — Componente lança `GenerativeComponentError` OU
  `GENERATION_MODE=disabled` (`component=None`) → fluxo não quebra,
  aciona o mesmo fallback determinístico de encaminhamento humano.
  *(Requisito 7)*
- **AC-07** — Qualquer turno resolvido pela fronteira generativa (AC-02,
  AC-03, AC-04, AC-06) grava `resolution_mode` correto
  (`local_didactic` | `fallback`) no resumo estruturado; turnos
  puramente numéricos gravam `deterministic`. *(Requisito 8)*
- **AC-08** — Texto de entrada com maiúsculas/minúsculas ou acentuação
  diferente produz a mesma classificação (normalização não muda o
  resultado). *(Requisito 2, suporte a AC-02/AC-03)*

## Restrições e invariantes

- `resolve_menu_option` e a árvore de transição de `flow._resolve_reply`
  continuam inalterados para entrada numérica.
- `RECENT_MESSAGE_LIMIT` (payload compacto) e a persona (`chat.persona`)
  continuam funcionando sem qualquer dependência do componente novo.
- O histórico bruto (`session.messages`) nunca é truncado — só o que é
  ENVIADO no payload é compactado (contrato herdado da Aula 2.5).
- Score é calculado por regras locais (frase forte = 1.0; 3+
  palavras-chave = 0.90; 2 = 0.80; 1 = 0.70; nenhuma = 0.0) em
  `local_generation.classify_intent` — **não representa uma
  probabilidade calibrada de nenhum modelo estatístico**, é apenas um
  número determinístico e reproduzível.
- Nenhum `import` de SDK de IA, cliente HTTP externo ou variável de
  ambiente de credencial existe em `app/chat/local_generation.py` ou
  `app/chat/generative.py`. `pyproject.toml` não lista dependência de
  provider de IA. `GENERATION_MODE=local_didactic` é o único modo com
  implementação real; `disabled` desliga a camada por completo.

## Riscos e limitações

- **Limitação conhecida** (proposital, não é bug a corrigir): a lista de
  frases/palavras-chave por intenção é pequena e didática — não é um
  sistema de linguagem natural completo.
- **Risco**: o score é uma tabela fixa de regras e não se recalibra com
  uso — uma frase real de usuário fora do vocabulário mapeado cai em
  `UNKNOWN` mesmo quando a intenção seria clara para um humano; não há
  teste que cubra vocabulário além do já mapeado nos 4 domínios.
- **Fora do escopo desta Spec** (decisão futura, não pendência): trocar
  `LocalDidacticComponent` por um provider real; abrir uma nova rodada de
  execução — esta revisão documenta o que já existe, não autoriza
  mudança de código.

## Matriz de rastreabilidade

| Critério | Requisito | Evidência (teste) |
|---|---|---|
| AC-01 | 1 | `test_greeting_does_not_call_component`, `test_numeric_option_does_not_call_component` |
| AC-02 | 2, 3, 8 | `test_classifies_technical_message`, `test_classifies_billing_message`, `test_classifies_account_message`, `test_recognized_free_text_generates_reply_and_ends_flow`, `test_recognized_free_text_records_fact_decision_and_preserves_history` |
| AC-03 | 4 | `test_returns_unknown_without_evidence`, `test_returns_unknown_on_tie_between_intents`, `test_unknown_intent_keeps_menu_state_and_uses_fallback` |
| AC-04 | 5 | `test_identifies_human_handoff_request`, `test_handoff_intent_uses_fixed_response` |
| AC-05 | 6 | `test_expected_intent_skips_reclassification` |
| AC-06 | 7 | `test_disabled_component_in_menu_uses_fallback`, `test_unavailable_component_in_domain_triggers_handoff_and_updates_summary` |
| AC-07 | 8 | `test_recognized_free_text_records_fact_decision_and_preserves_history`, `test_unavailable_component_in_domain_triggers_handoff_and_updates_summary` |
| AC-08 | 2 | `test_normalize_removes_case_and_accents` |

Todo requisito tem pelo menos um critério e todo critério tem pelo menos
um teste — nenhuma linha da matriz fica vazia.

## Evidências

40 testes passando (24 anteriores + 16 da evolução generativa), sem
acesso a rede, sem chave, sem custo:

- `tests/test_local_generation.py` (8 testes): `test_normalize_removes_case_and_accents`,
  `test_classifies_technical_message`, `test_classifies_billing_message`,
  `test_classifies_account_message`, `test_identifies_human_handoff_request`,
  `test_returns_unknown_without_evidence`, `test_returns_unknown_on_tie_between_intents`,
  `test_expected_intent_skips_reclassification`.
- `tests/test_generative_flow.py` (8 testes): `test_greeting_does_not_call_component`,
  `test_numeric_option_does_not_call_component`,
  `test_recognized_free_text_generates_reply_and_ends_flow`,
  `test_recognized_free_text_records_fact_decision_and_preserves_history`,
  `test_unknown_intent_keeps_menu_state_and_uses_fallback`,
  `test_handoff_intent_uses_fixed_response`,
  `test_disabled_component_in_menu_uses_fallback`,
  `test_unavailable_component_in_domain_triggers_handoff_and_updates_summary`.

## Status retroativo

Esta Spec (3.3 + refinamento 3.4) descreve uma evolução **já implementada
e já mergeada** (Aula 2.8). Nenhuma das duas versões autoriza uma nova
execução — servem como material de revisão e como exemplo didático de
como uma Spec retroativa evolui de "correta" para "verificável". Tags da
implementação original: `m02-a08-start` → `m02-a08-end`, branch
`lesson/m02-a08-primeira-evolucao-generativa`, já mergeada em `main`
(merge commit da Aula 2.8).
