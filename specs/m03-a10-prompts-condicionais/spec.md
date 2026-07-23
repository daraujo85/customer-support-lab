# Spec — Montagem condicional de prompts

> **Status: `prospectiva`** (mesma convenção das aulas anteriores): escrita
> ANTES da implementação, autorizando e delimitando a mudança.

## Contexto e problema

Desde a Aula 3.9, toda inferência real recebe exatamente a mesma instrução
de tarefa (`prompts/task_instruction.md`) — não importa se a intenção
aceita foi suporte técnico, financeiro ou informações de conta. Isso é
suficiente pra regras GERAIS (idioma, limite de frases, segurança), mas não
pra regras que só fazem sentido numa área: o que é uma orientação segura de
suporte técnico (não pedir pra abrir o equipamento) não tem nada a ver com
o que é uma orientação segura financeira (não confirmar estorno sem
evidência).

## Objetivo

O prompt enviado ao modelo passa a ser MONTADO a partir de dois pedaços: o
template-base (comum a todas as áreas) mais um bloco específico da
intenção JÁ ACEITA pela classificação determinística. A condição é
escolhida pelo CÓDIGO — o modelo nunca escolhe qual bloco usar, e nunca vê
os blocos das outras áreas.

**Frase-guia:** montagem condicional não significa deixar o modelo
escolher o prompt. O código escolhe os blocos; o modelo recebe somente o
contexto autorizado pra tarefa.

## Escopo

**Dentro do escopo:**
- Três novos artefatos de bloco específico, um por intenção que gera
  inferência real: `prompts/intents/suporte_tecnico.md`,
  `prompts/intents/financeiro.md`, `prompts/intents/informacoes_conta.md`.
  Sem arquivo para `unknown`/`human_handoff` — essas intenções nunca
  chegam a montar prompt nenhum (resolvidas antes, sem chamada ao modelo).
- `app/chat/prompt_loader.py` ganha `PromptBundle` (dataclass congelada:
  `task_template` + `intent_instructions`) e `load_prompt_bundle()`, que
  carrega e valida o template-base E os três blocos específicos. O loader
  continua só lendo e validando arquivo — não decide seleção nem combina
  nada.
- Novo módulo puro `app/chat/prompt_builder.py` —
  `build_task_instruction(bundle, intent)` seleciona o bloco certo e monta
  a instrução final (base renderizada + bloco específico). Sem leitura de
  disco, sem rede, sem acesso a sessão, sem classificação — só composição
  determinística de string.
- `OllamaGenerativeComponent` passa a receber um `PromptBundle` completo
  (em vez de um template único já renderizável) e chama
  `build_task_instruction` a cada `generate()`, usando a intenção já
  decidida (classificada ou `expected_intent`).
- `app/main.py` chama `load_prompt_bundle()` no lugar de
  `load_prompt_template()`, ainda só no modo `ollama`.
- Fail-fast preservado: qualquer artefato ausente/vazio/inválido (base OU
  bloco específico) derruba o boot no modo `ollama`. `local_didactic` e
  `disabled` continuam independentes.

**Fora do escopo (explicitamente, decisão futura):**
- Condição escolhida pelo modelo, ou baseada em palavras do usuário.
- RAG ou documentos externos.
- Tools, saída estruturada, classificação por LLM.
- Troca de modelo por área, múltiplos idiomas.
- Prompts em banco de dados, hot reload, A/B testing, painel de edição.

## Requisitos funcionais

1. Toda inferência real aplica o template-base (comportamento herdado da
   3.9, sem mudança de texto).
2. Suporte técnico recebe EXCLUSIVAMENTE o bloco de suporte técnico.
3. Financeiro recebe EXCLUSIVAMENTE o bloco financeiro.
4. Informações de conta recebe EXCLUSIVAMENTE seu bloco.
5. Nenhum bloco de uma área aparece no payload de outra área.
6. `UNKNOWN` e `HUMAN_HANDOFF` não montam prompt nem chamam rede (herdado
   da 3.8/3.9, preservado).
7. `expected_intent` seleciona o bloco certo sem reclassificar.
8. Bundle incompleto ou inválido (template-base OU qualquer bloco
   ausente/vazio/com placeholder indevido) derruba o boot no modo
   `ollama`.
9. `local_didactic` e `disabled` continuam subindo normalmente
   independente dos artefatos de prompt.
10. A instrução montada continua entrando ANTES da última mensagem do
    usuário, nunca depois (correção da 3.8, preservada).
11. Nenhum teste acessa rede real.
12. Validação manual confirma o comportamento nas três áreas (payload real
    mostrando o bloco correto por intenção).

## Restrições e invariantes (o que continua igual)

- Classificação de intenção, score, `MIN_ACCEPTED_SCORE=0,70`, máquina de
  estados, fallback e resumo estruturado continuam exatamente como antes.
- `ResolutionMode.OLLAMA`, `temperature=0`, `seed=42`, `stream=false` não
  mudam.
- `Dockerfile`, `docker-compose.yml`, `app/chat/flow.py`,
  `app/chat/generative.py`, `app/chat/local_generation.py`,
  `app/chat/payload.py` e `app/chat/summary.py` não mudam. O Dockerfile já
  copia `prompts/` inteiro (decisão da 3.9) — os blocos novos entram
  automaticamente, sem editar a imagem.

## Riscos e limitações

- **Risco aceito conscientemente**: mais um arquivo por área significa
  mais um lugar onde uma regra pode divergir do texto-base — os testes de
  "não vazamento" (`test_prompt_builder.py`) existem exatamente pra pegar
  isso cedo.
- **Fora do escopo, não um bug**: nenhuma seleção dinâmica pelo modelo,
  nenhum aprendizado — a condição é sempre um `if`/lookup determinístico
  no código, nunca uma decisão do LLM.

## Evidências esperadas (a preencher depois da implementação)

- `tests/test_prompt_loader.py`: carrega os três blocos oficiais, erros
  claros para bloco ausente/vazio/com placeholder indevido/UTF-8 inválido.
- `tests/test_prompt_builder.py`: cada intenção recebe seu bloco e só o
  seu; base sempre antes do bloco específico; `UNKNOWN`/`HUMAN_HANDOFF`
  rejeitados; montagem determinística (mesma entrada, mesma saída).
- `tests/test_ollama_generation.py`: intenção técnica/financeira só levam
  sua própria orientação no payload; `expected_intent` seleciona sem
  reclassificar; ordem das mensagens preservada.
- `tests/test_main_generation_mode.py`: modo `ollama` falha rápido quando
  qualquer artefato (base ou bloco) é inválido; `local_didactic`/`disabled`
  não dependem de nenhum deles.
- Suíte completa passando.
- Validação manual: uma pergunta de cada área rodando contra o Ollama real,
  confirmando o bloco correto na instrução enviada.

## Tags desta evolução

Branch `lesson/m03-a10-prompts-condicionais`, tags `m03-a10-start` →
`m03-a10-end`, a partir do fim da Aula 3.9 (`m03-a09-end`/merge em `main`).
