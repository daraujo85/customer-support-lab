# Aula 2.5 — Resumo de conversa

```text
Branch: lesson/m02-a05-resumo-conversa
Base: tag m02-a05-start (a partir da main, no estado de m02-a03-end — a
      Aula 2.4 "Janela de contexto" não alterou o repositório)
Alteração no laboratório: resumo ESTRUTURADO (fatos/decisões/pendências/
      preferências) atualizado por regra de transição de estado; payload
      passa a levar persona + resumo + só as mensagens recentes quando o
      histórico passa do limite didático
Commit: commits pequenos, mergeados --no-ff na main
```

## Objetivo prático

Desde a Aula 2.1, `build_payload` manda **toda** a conversa a cada rodada. A
Aula 2.4 já explicou o PROBLEMA (janela de contexto finita); esta aula
implementa a solução: quando o histórico passa de um limite pedagógico de
mensagens recentes, as mais antigas deixam de ser enviadas cruas — mas
**não são descartadas da sessão**. Um resumo ESTRUTURADO (não um resumo de
texto livre) é atualizado a cada transição de estado, com quatro
responsabilidades distintas:

- **Fatos** — o que o usuário informou explicitamente (formulação sempre
  "Usuário informou...", nunca afirmando que o dado é válido).
- **Decisões** — o que o fluxo determinístico decidiu de fato (área
  selecionada, encerramento) — nunca o que o sistema só sugeriu.
- **Pendências** — o que ainda está em aberto (sempre uma pendência ativa
  por vez, substituída a cada transição).
- **Preferências** — vazio nesta aula (o laboratório não tem fluxo próprio
  pra capturar preferência); o campo existe desde já pro modelo suportar,
  mas não é inferido por estilo de escrita.

**Sem chamar nenhuma IA** — a primeira chamada generativa continua reservada
pra Aula 2.8.

## O que foi alterado (só isto)

```text
app/chat/state.py       — NOVO: ConversationSummary (facts/decisions/pending/
                           preferences); Session ganha summary: ConversationSummary
app/chat/summary.py     — NOVO: update_summary(session, previous_state, user_input)
                           + render_summary(summary) — regra por transição de estado
app/chat/payload.py     — NOVO: RECENT_MESSAGE_LIMIT = 4 + build_system_context(session)
                           build_payload compacta (persona + resumo + últimas
                           RECENT_MESSAGE_LIMIT mensagens) só quando necessário
app/chat/flow.py        — handle_input captura o estado anterior e chama
                           update_summary(...) depois da transição
tests/test_summary.py   — NOVO: 8 testes (pendência de saudação, decisão+pendência
                           de opção válida, entrada inválida sem decisão, fato+
                           limpeza de pendência, handoff humano mantém pendência,
                           preferências nunca inferidas, payload curto inalterado,
                           payload longo compactado com histórico bruto preservado)
```

Não alterado: `app/chat/persona.py`, `app/main.py`, `app/static/*`,
`Dockerfile`, `docker-compose.yml`, `pyproject.toml`.

## Por que resumo estruturado, não resumo de texto livre

Um resumo de texto livre (parágrafo corrido) esconde a responsabilidade de
cada informação — fica difícil saber se algo é um fato confirmado, uma
decisão do sistema ou uma pendência aberta. Separar em quatro campos
tipados torna o contrato **observável e testável**: dá pra afirmar
"pendências está vazio" ou "há exatamente uma decisão" sem parsear texto.
`render_summary` só entra na hora de montar o payload textual — internamente
o resumo é sempre uma estrutura de dados.

## `Session.messages` nunca é apagado

Diferente de uma implementação ingênua que "trunca" o histórico, aqui
`session.messages` continua guardando TODAS as mensagens da sessão — é
`build_payload` quem decide, na hora de montar o payload, enviar só as
últimas `RECENT_MESSAGE_LIMIT`. A compactação reduz o que é ENVIADO, não o
que é GUARDADO.

## Payload real de exemplo (rodado durante a implementação)

Depois de 3 rodadas (greeting → opção 1 "Suporte técnico" → "meu computador
não liga" = 6 mensagens, 2 acima do limite):

```json
[
  {
    "role": "system",
    "content": "Você é o Assistente de Atendimento da Customer Support Lab.\n\n[...persona completa da Aula 2.3...]\n\nCONTEXTO RESUMIDO DA SESSÃO\nRESUMO DA CONVERSA\n\nFATOS\n- Usuário informou problema técnico: meu computador não liga.\n\nDECISÕES\n- Área de atendimento selecionada: Suporte técnico.\n- Atendimento determinístico encerrado após coleta da informação.\n\nPENDÊNCIAS\n- Nenhuma pendência registrada.\n\nPREFERÊNCIAS\n- Nenhuma preferência explícita registrada."
  },
  {"role": "user", "content": "1"},
  {"role": "assistant", "content": "Você está em Suporte técnico. Descreva o problema em poucas palavras que um atendente vai te responder em instantes."},
  {"role": "user", "content": "meu computador não liga"},
  {"role": "assistant", "content": "Obrigado pelo contato! Se precisar de algo mais, é só chamar de novo."}
]
```

A saudação (2 primeiras mensagens) saiu do payload cru, mas o fato/decisão
relevantes continuam presentes — de forma estruturada, não como cópia da
transcrição.

## Validação (real, rodada a cada etapa)

```bash
docker compose build app
docker compose run --rm app python -m pytest -v
# 24 passed (16 anteriores + 8 novos de test_summary.py)
```

Validação manual: `docker compose up --build`, abrir `http://localhost:8010`,
clicar "Ver payload", enviar mensagens até passar de 2 rodadas, e confirmar
que o `system` passa a trazer "CONTEXTO RESUMIDO DA SESSÃO" com as quatro
seções, e que o payload nunca cresce além de `system + 4 mensagens`.

## O que permanece exatamente igual

- O menu e as respostas visíveis continuam 100% determinísticos.
- Nenhuma chamada de LLM existe ainda — reservado pra Aula 2.8.
- A persona (Aula 2.3) continua igual; só ganha a seção extra de resumo
  quando há compactação.

## Fluxo git usado

```bash
git switch main
git pull
git tag m02-a05-start
git switch -c lesson/m02-a05-resumo-conversa
# commits pequenos (acima)
git switch main
git merge --no-ff lesson/m02-a05-resumo-conversa
git tag m02-a05-end
git push origin main --tags
```

## Como isso conecta os fundamentos (pra narração)

- **Resumo não é geração** — é puramente estrutural (regra de transição de
  estado), porque ainda não existe LLM no laboratório. Quando a Aula 2.8
  trouxer geração real, esse MESMO ponto de compactação poderia
  opcionalmente virar um resumo generativo — mas a estratégia (fatos,
  decisões, pendências, preferências) já está pronta e testada antes de
  qualquer IA entrar.
- **Sem antecipar módulos futuros** — nada de estado de sessão/usuário/
  execução (2.6), nada de geração real (2.8).
- **Gancho direto pra 2.6** — o resumo vive dentro de `Session`, que ainda é
  só um dicionário em memória; a separação entre estado de usuário, sessão e
  execução (2.6) é quem decide ONDE isso deveria realmente morar.

## Entrega da aula (pra narração)

> Histórico infinito não é opção. Um resumo estruturado — fatos, decisões,
> pendências, preferências — é uma decisão de arquitetura tomada ANTES de
> qualquer chamada de LLM existir. A geração real só vai precisar respeitar
> essa estrutura, não inventá-la.

O laboratório troca "manda tudo sempre" por um contrato observável: quatro
campos tipados que sobrevivem à compactação do payload — o mesmo
comportamento determinístico de sempre, agora com controle real de contexto.
