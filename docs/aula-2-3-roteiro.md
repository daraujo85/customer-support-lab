# Aula 2.3 — Persona não é fantasia

```text
Branch: lesson/m02-a03-persona-assistente
Base: tag m02-a03-start (a partir da main, pois a Aula 2.2 não alterou o
      repositório — main já estava no estado de m02-a01-end)
Alteração no laboratório: mensagem system deixa de ser uma frase solta e
      passa a vir de uma persona explícita (identidade, escopo, tom,
      vocabulário e limites)
Commit: 3 commits pequenos, mergeados --no-ff na main
```

## Objetivo prático

Desde a Aula 2.1, `SYSTEM_PROMPT` era uma frase genérica escrita direto em
`payload.py`: `"Você é o assistente de atendimento ao cliente."` — suficiente
pra demonstrar que a mensagem `system` entra primeiro no payload (Aula 2.2),
mas incapaz de comunicar identidade, escopo, tom, vocabulário ou limites de
verdade. O objetivo desta aula é transformar essa frase solta num **contrato
explícito** — persona como dados (`Persona`), não como fantasia/personalidade
decorativa. Ainda não existe LLM, entrada livre, geração, provider ou
inferência — isso continua reservado pra Aula 2.8.

## O que foi alterado (só isto)

```text
app/chat/persona.py      — NOVO: Persona (dataclass) + CUSTOMER_SUPPORT_PERSONA
                            + build_system_prompt(persona)
app/chat/payload.py      — SYSTEM_PROMPT passa a vir de build_system_prompt(...)
tests/test_persona.py    — NOVO: 4 testes (contrato da persona, seções do
                            prompt, limites de segurança, payload usa a persona)
```

Não alterado: `app/chat/state.py`, `app/chat/flow.py`, `app/main.py`,
`app/static/*`, `Dockerfile`, `docker-compose.yml`, `pyproject.toml` — zero
dependência nova, zero mudança de interface (o painel "Ver payload" já
mostrava o conteúdo completo da mensagem `system`).

## Persona não é fantasia

A persona **não tem nome humano fictício** de propósito — isso reforça o
título da aula. O que importa é o contrato funcional:

```python
@dataclass(frozen=True)
class Persona:
    identity: str
    scope: tuple[str, ...]
    tone: tuple[str, ...]
    vocabulary: tuple[str, ...]
    boundaries: tuple[str, ...]
```

`build_system_prompt` monta a mensagem `system` de forma **tradicional e
determinística** — nunca pedindo pra uma IA gerar a própria persona.

## Payload real de exemplo (rodado durante a implementação)

```json
[
  {"role": "system", "content": "Você é o Assistente de Atendimento da Customer Support Lab.\n\nESCOPO\n- Orientar solicitações de suporte técnico.\n- Orientar questões de faturamento.\n- Orientar consultas sobre informações de conta.\n- Indicar encaminhamento para atendimento humano quando necessário.\n\nTOM\n- Seja cordial.\n- Seja direto e claro.\n- Evite respostas excessivamente longas.\n\nVOCABULÁRIO\n- Responda em português do Brasil.\n- Use frases curtas.\n- Evite jargão técnico desnecessário.\n\nLIMITES\n- Não invente dados de clientes, pedidos, faturas, contas ou políticas.\n- Não afirme que consultou sistemas ou executou ações que não aconteceram.\n- Não tome decisões de negócio que não foram autorizadas pela aplicação.\n- Quando faltar informação, capacidade ou permissão, informe o limite.\n- Quando necessário, indique encaminhamento para atendimento humano."},
  {"role": "user", "content": ""},
  {"role": "assistant", "content": "Bom dia! Bem-vindo ao suporte. Como posso te ajudar hoje?\n\nEscolha uma opção:\n1. Suporte técnico\n2. Questões de faturamento\n3. Informações de conta\n4. Falar com um atendente"},
  {"role": "user", "content": "1"},
  {"role": "assistant", "content": "Você está em Suporte técnico. Descreva o problema em poucas palavras que um atendente vai te responder em instantes."}
]
```

## Validação (real, rodada a cada etapa)

```bash
docker compose build app
docker compose run --rm app python -m pytest -v
# 16 passed (12 anteriores + 4 novos de test_persona.py)
```

Validação manual: `docker compose up --build`, abrir `http://localhost:8010`,
clicar "Ver payload", confirmar que `system` mostra a persona completa,
enviar `1` e confirmar que as mensagens `user`/`assistant` continuam entrando
na ordem correta e que a resposta determinística de suporte não mudou
(confirmado via `curl` no endpoint `/api/chat` durante a implementação).

## O que permanece exatamente igual

- O menu e as respostas visíveis continuam 100% determinísticos.
- Opção 1 → suporte técnico · Opção 2 → faturamento · Opção 3 → informações
  de conta · Opção 4 → encaminhamento humano · entrada inválida → repete o menu.
- Mensagem pedagógica: **persona controla identidade/escopo/tom/vocabulário/
  limites de comunicação; regras críticas de negócio continuam no código
  determinístico.**

## Fluxo git usado

```bash
git switch main
git pull
git tag m02-a03-start
git switch -c lesson/m02-a03-persona-assistente
# 3 commits pequenos (acima)
git switch main
git merge --no-ff lesson/m02-a03-persona-assistente
git tag m02-a03-end
git push origin main --tags
```

## Como isso conecta os fundamentos (pra narração)

- **Persona não é fantasia** — não é personalidade decorativa nem nome
  fictício; é identidade funcional + escopo + tom + vocabulário + limites,
  como dados explícitos e testáveis.
- **Sem antecipar módulos futuros** — ainda nenhuma LLM é chamada (Aula 2.8);
  nada de resumo/histórico (2.5); nada de estado de sessão/execução (2.6).
- **Gancho direto pra 2.8** — quando a primeira chamada generativa existir,
  a persona que a orienta já é exatamente essa que o aluno está vendo no
  painel desde a 2.3.

## Entrega da aula (pra narração)

> Persona controla identidade, escopo, tom, vocabulário e limites de
> comunicação. Regras críticas de negócio continuam no código determinístico.

O laboratório troca uma frase genérica por um contrato explícito — o mesmo
comportamento determinístico de sempre, mas agora com uma persona de verdade
orientando a conversa.
