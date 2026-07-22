# Spec — Contexto em camadas e primeira inferência real

> **Status: `prospectiva`.** Esta é a primeira Spec do projeto escrita ANTES
> da implementação (as anteriores, em
> `specs/m02-a08-primeira-evolucao-generativa/`, foram retroativas). O
> objetivo aqui é autorizar e delimitar uma mudança real: a primeira conexão
> do laboratório com uma LLM de verdade (Ollama), rodando localmente, sem
> custo e sem API paga.

## Contexto e problema

Desde a Aula 2.8, a fronteira generativa do laboratório é simulada por
`LocalDidacticComponent` — regras determinísticas, sem nenhuma inferência
real. As Aulas 3.5 a 3.7 validaram, FORA do laboratório, que o Ollama roda
bem no Mac (`llama3.2:1b`, 1.3 GB) e explicaram runtime, hardware e modelos
por tarefa. Chegou a hora de conectar essa capacidade real ao chatbot.

## Objetivo

Introduzir um segundo modo de geração (`GENERATION_MODE=ollama`) que produz
o TEXTO da resposta com uma LLM real via Ollama — mantendo a classificação
de intenção, o score de confiança e a decisão de transição de estado
inteiramente determinísticos, exatamente como hoje.

**Frase-guia:** a LLM escreve a resposta; o código continua decidindo
quando chamá-la, qual intenção foi aceita, qual estado muda e o que
acontece quando ela falha.

## Escopo

**Dentro do escopo:**
- Novo componente `OllamaGenerativeComponent` (`app/chat/ollama_generation.py`),
  implementando o mesmo `Protocol GenerativeComponent` já existente.
- Classificação de intenção continua 100% por `classify_intent()`
  (determinístico) — o Ollama só é chamado quando a classificação já
  aceitou uma intenção (score ≥ `MIN_ACCEPTED_SCORE`, não-UNKNOWN,
  não-HUMAN_HANDOFF).
- Em domínio já conhecido (`expected_intent` preenchido), o componente não
  reclassifica — só chama o Ollama pra gerar a resposta daquele domínio.
- O contexto em camadas já construído (`build_payload`/
  `build_generative_messages` — persona, resumo, histórico recente, entrada
  atual) passa a ser REALMENTE enviado ao modelo (antes, o componente local
  podia ignorá-lo internamente).
- Uma instrução curta de tarefa (system prompt), como constante no próprio
  `ollama_generation.py` — deliberadamente ainda não extraída como artefato
  versionado (isso fica pra uma aula futura de prompts).
- Configuração via variáveis de ambiente: `OLLAMA_BASE_URL`
  (`http://host.docker.internal:11434` default), `OLLAMA_MODEL`
  (`llama3.2:1b` default), `OLLAMA_TIMEOUT_SECONDS` (`60` default),
  `OLLAMA_NUM_CTX` (`2048` default).
- Opções de geração fixas na chamada: `temperature=0`, `seed=42`,
  `stream=false` — reduzem variação, mas não prometem reprodução byte a
  byte entre versões/máquinas.
- Tratamento de falha: qualquer erro de rede, timeout, status HTTP
  inválido, corpo malformado ou resposta vazia vira
  `GenerativeComponentError` — o fluxo já sabe cair no fallback
  determinístico existente.
- Novo `ResolutionMode.OLLAMA`, registrado no resumo estruturado quando o
  turno foi resolvido por essa via.
- `httpx` deixa de ser dependência só de desenvolvimento e passa a
  dependência principal do projeto.

**Fora do escopo (explicitamente, decisão futura):**
- Classificação de intenção ou score calculados pelo LLM.
- Saída estruturada (JSON/schema) pedida ao modelo.
- Streaming de resposta.
- Retry automático em caso de falha.
- RAG, ferramentas (tool calling) ou qualquer orquestração multi-etapa.
- Uso do desktop remoto (192.168.31.231) — esta aula usa só o Mac.
- Extrair o prompt/instrução de tarefa como artefato versionado — o texto
  fica como constante no código por enquanto, de propósito (a dor de tê-lo
  embutido no código é o gancho pedagógico da próxima evolução de
  contexto).
- Qualquer mudança na interface (`app/static/*`) ou no contrato de payload
  das aulas anteriores.
- Health-check do Ollama no boot da aplicação — o app deve subir mesmo com
  o Ollama desligado; a primeira falha real é que aciona o fallback.

## Requisitos funcionais

1. `GENERATION_MODE=ollama` no ambiente constrói um
   `OllamaGenerativeComponent` configurado pelas variáveis de ambiente
   acima; `local_didactic` e `disabled` continuam funcionando exatamente
   como antes.
2. Texto livre no menu principal continua classificado por
   `classify_intent()` — o Ollama só entra em jogo quando essa
   classificação já aceitou uma intenção.
3. UNKNOWN e HUMAN_HANDOFF classificados deterministicamente **não**
   chamam o Ollama — seguem os caminhos já existentes (fallback do menu e
   resposta fixa de handoff, respectivamente).
4. Em domínio já conhecido (`expected_intent` presente), o score é `1.0`
   e nenhuma reclassificação acontece — só a chamada ao modelo pra gerar
   o texto.
5. A chamada ao Ollama usa `POST /api/chat` com o modelo, as mensagens do
   contexto em camadas (persona + resumo + histórico recente + entrada
   atual, mais a instrução curta de tarefa), `stream=false` e as opções
   `temperature=0`, `seed=42`, `num_ctx` configurável.
6. Qualquer falha da chamada (conexão, timeout, status HTTP, corpo
   inválido, `message.content` ausente ou vazio) vira
   `GenerativeComponentError`, e o fluxo aciona o mesmo fallback
   determinístico já usado quando o componente local didático falha.
7. O resumo estruturado (`chat.summary`) registra `ResolutionMode.OLLAMA`
   quando o turno foi resolvido por essa via, preservando as demais regras
   de fatos/decisões/pendências já estabelecidas.
8. Nenhum teste automatizado faz chamada de rede real ao Ollama — os
   testes usam um cliente HTTP injetável (transporte falso).

## Restrições e invariantes (o que continua igual)

- Porta `8010`, saudação, opções numéricas `1`-`4`, máquina de estados,
  `Intent`, `MIN_ACCEPTED_SCORE=0.70`, handoff com resposta fixa,
  `local_didactic` e `disabled` continuam funcionando sem alteração de
  comportamento.
- Histórico bruto (`session.messages`) nunca é truncado; resumo
  estruturado e o limite de 4 mensagens recentes no payload continuam
  determinísticos.
- Fallback em indisponibilidade do componente continua acionando
  `HUMAN_HANDOFF` exatamente como hoje.
- Nenhuma credencial, nenhum uso do desktop remoto.

## Riscos e limitações

- **Risco aceito conscientemente**: a partir desta aula, o TEXTO da
  resposta deixa de ser 100% reproduzível — pode variar em palavras,
  estrutura de frase e latência entre execuções, mesmo com
  `temperature=0`/`seed` fixos (não há garantia de determinismo perfeito
  entre versões do Ollama/modelo). O que continua determinístico é o
  FLUXO: intenção aceita, score, estado seguinte e comportamento de
  fallback.
- **Limitação conhecida**: o prompt/instrução de tarefa vive como
  constante no código, não como artefato versionado — proposital, vira
  dor pedagógica da próxima aula de contexto.
- **Fora do escopo, não um bug**: sem retry, sem streaming, sem
  classificação por LLM.

## Evidências (preenchidas após a implementação)

- `tests/test_ollama_generation.py` (12 testes): chamada correta ao
  `/api/chat`, payload com contexto em camadas, opções de geração corretas,
  score/intenção preservados da regra, `expected_intent` não reclassifica,
  UNKNOWN/HUMAN_HANDOFF não chamam rede, falhas de rede/timeout/status/
  corpo viram `GenerativeComponentError` — tudo com `httpx.MockTransport`,
  sem rede real.
- `tests/test_generative_flow.py`: turno com `source="ollama"` encerra o
  fluxo, resumo registra `ResolutionMode.OLLAMA` (distinto de
  `LOCAL_DIDACTIC`), falha do componente aciona fallback, caminho numérico
  continua sem chamar o componente.
- `tests/test_main_generation_mode.py` (8 testes): `local_didactic`
  (default e explícito), `disabled`, `ollama` (defaults e overrides via
  env), modo desconhecido, timeout/contexto/modelo inválidos.
- Suíte completa: **66 testes passando** (40 existentes + 26 novos).
- **Validação manual end-to-end** (`GENERATION_MODE=ollama docker compose up
  --build`, modelo real `llama3.2:1b` local):
  - Texto livre reconhecido no menu → resposta real gerada pelo modelo,
    intenção/score determinísticos preservados.
  - Domínio já conhecido (`expected_intent`) → modelo chamado só pra gerar
    o texto, sem reclassificar.
  - Opção numérica → nenhuma chamada ao Ollama (resposta fixa).
  - Ollama indisponível (`OLLAMA_BASE_URL` apontando pra porta fechada) →
    app não crasha, cai no fallback determinístico existente.
  - Revertendo pra `GENERATION_MODE=local_didactic` (default) → comportamento
    idêntico ao de antes desta aula.
- **Bug real encontrado e corrigido durante a validação manual** (não nos
  testes com double, só apareceu com o modelo de verdade): a instrução de
  tarefa era anexada como mensagem `system` DEPOIS da mensagem do usuário —
  terminar a lista de mensagens numa mensagem `system` quebra o template de
  chat do Llama (que espera responder a um turno de usuário), e o modelo
  devolvia os marcadores de template como texto literal
  (`<|start_header_id|>assistant<|end_header_id|>`) em vez de só a resposta.
  Corrigido em `_add_task_instruction`: a instrução agora entra ANTES da
  última mensagem, não depois.

## Tags desta evolução

Branch `lesson/m03-a08-contexto-em-camadas`, tags `m03-a08-start` →
`m03-a08-end`, a partir de `main` (mesmo ponto de `m03-a04-end`, já que
3.5-3.7 não alteraram o repositório).
