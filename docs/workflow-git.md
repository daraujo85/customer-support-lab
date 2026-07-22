# Fluxo de git por aula — branch + tags

**Regra fundamental (corrigida em 2026-07-17): branch não existe porque existe
aula. Branch existe porque existe mudança real no repositório.** O laboratório
aparecer na tela, ser lido ou ser explicado pelo Claude Code não é motivo pra
branch — só commit de verdade é.

## As três categorias de aula

| Tipo de aula | Usa o laboratório | Altera repositório | Branch |
|---|---:|---:|---:|
| Conceitual | talvez | não | não |
| Demonstração e leitura | sim | não | não |
| Evolução prática | sim | sim | sim |

Uma aula "de demonstração e leitura" pode ter o Claude Code lendo arquivos,
explicando arquitetura, respondendo perguntas sobre o código, até mostrando um
plano **hipotético** — nada disso passa por `git commit`, então não tem
branch. Só quando algo é de fato escrito no repositório (código, teste,
config, documentação do laboratório) é que a aula ganha
`lesson/mXX-aYY-slug` + tags `start`/`end`.

## Módulo 1

| Aula | Uso do laboratório | Branch |
|---|---|---|
| 1.1 — Este curso não é sobre ferramentas | apenas apresentação | nenhuma |
| 1.2 — Programação, engenharia e responsabilidade | referência conceitual | nenhuma |
| 1.3 — Chatbot determinístico | criação do projeto | `lesson/m01-a03-chatbot-deterministico` |
| 1.4 — Do codador ao orquestrador | leitura e análise do código existente | nenhuma |
| 1.5 — Human in the Loop | análise dos pontos de aprovação | nenhuma |
| 1.6 — Fundamentos que permanecem (DDD, testes, arquitetura, DevOps, SDD) | refatoração pequena e protegida por testes | `lesson/m01-a06-fundamentos-engenharia` |
| 1.7 — O curso como prova do método | demonstração da esteira de produção | nenhuma |
| 1.8 — Prova e reflexão | nenhuma evolução | nenhuma |

A Aula 1.3 foi commitada direto na `main` (antes deste padrão existir) — o fim
dela ficou marcado retroativamente com a tag `m01-a03-end` e a branch
`lesson/m01-a03-chatbot-deterministico` (apontando pro mesmo commit da `main` —
é um marcador retroativo, não representa um fluxo isolado de verdade, já que o
trabalho já tinha acontecido direto na `main`).

A Aula 1.4 — Do codador ao orquestrador — usa o laboratório **só como objeto
de análise**: leitura, explicação, perguntas, comparação de um pedido vago com
um pedido bem contextualizado, plano hipotético. Nenhum arquivo é alterado,
então não tem branch, não tem commit — ver `docs/aula-1-4-roteiro.md`. (Uma
primeira tentativa desta aula chegou a criar um teste só pra ter algo pra
commitar e justificar uma branch — foi revertido por ser pedagogicamente
errado: o motivo tem que vir da aula, não a branch justificar a si mesma.)

A tabela em "Plano de branches do curso inteiro" (abaixo) lista as aulas dos
demais módulos com evolução funcional de verdade — a primeira é a 2.1.

## Por que branch + tag, não só branch solta

Uma branch por aula sem merge na `main` faz o laboratório divergir — cada aula
vira uma ilha e o projeto deixa de contar uma história contínua. O fluxo certo:

```
main
 └── lesson/m02-a01-payload-conversacao
       └── merge (--no-ff) em main
 └── lesson/m02-a03-persona-assistente
       └── merge (--no-ff) em main
```

A `main` sempre representa a evolução OFICIAL do laboratório. As tags marcam os
checkpoints exatos usados na gravação — elas não mudam nunca (branch pode receber
commit novo ou ser apagada depois do merge; a tag não).

## Passo a passo por aula

**1. Antes de gravar** — a branch da aula sempre deriva do estado da aula
anterior, não de um `main` genérico. Na prática, como cada aula termina com
merge `--no-ff` na `main` (passo 3), a `main` pós-merge da aula anterior **é**
o estado da aula anterior — então `git checkout main && git pull` continua
sendo o comando certo, desde que seja feito logo após o merge/tag da aula
anterior, sem outros commits não relacionados no meio. Se por algum motivo a
`main` recebeu commits fora da sequência de aulas (ex.: docs, hotfix), derive
explicitamente da tag de fim da aula anterior em vez de `main`:

```bash
git checkout m01-a03-end          # tag de fim da ÚLTIMA aula que gerou branch — não "main" às cegas
git tag m02-a01-start
git checkout -b lesson/m02-a01-payload-conversacao
```

O laboratório é uma linha do tempo contínua: cada aula com branch evolui
exatamente de onde a última aula-com-branch parou. Aulas conceituais ou de
demonstração (sem commit — ex. 1.4, 1.5) não entram nessa cadeia porque não
geram tag: a próxima aula com branch (2.1) deriva direto de `m01-a03-end`, não
de uma tag inexistente da 1.4.

**2. Durante a gravação** — o Claude Code (real ou shim, conforme o caso — ver
`docs/aula-1-3-roteiro.md` sobre quando usar shim) altera os arquivos nessa
branch. Comitar em pedaços pequenos, um por etapa visível da aula, não um commit
gigante no final:

```
chore: cria estrutura inicial do laboratório
feat: adiciona máquina de estados determinística
feat: cria interface web do atendimento
test: valida menu e transições
docs: documenta arquitetura da aula
```

Isso facilita mostrar a evolução, revisar decisão por decisão e até regravar só
um pedaço da aula sem mexer no resto.

**3. Depois de revisar o diff e rodar os testes, aprova:**

```bash
git checkout main
git merge --no-ff lesson/m02-a01-payload-conversacao
git tag m02-a01-end
git push origin main --tags
```

## Convenção de nomes

Branch: `lesson/<módulo>-<aula>-<slug-curto-do-tema>`
```
lesson/m01-a03-chatbot-deterministico
lesson/m02-a01-payload-conversacao
lesson/m02-a08-primeira-evolucao-generativa
lesson/m03-a03-sdd-tlc-spec-driven
```

Tags: `m<módulo com 2 dígitos>-a<aula com 2 dígitos>-start` / `-end`
```
m01-a03-start / m01-a03-end
m02-a01-start / m02-a01-end
```

## Comandos úteis

Comparar o que uma aula mudou:
```bash
git diff m02-a01-start m02-a01-end
```

Voltar pro estado exato de antes de uma aula (ex.: pra regravar):
```bash
git checkout m02-a01-start
```

## Plano de branches do curso inteiro

Nem toda aula mexe no laboratório — só as que **criam, alteram, configuram ou
validam** alguma parte dele ganham branch própria. Aulas puramente conceituais
ficam de fora (continuam só narração/slides, sem tocar o repo). Tabela definida
pelo Diego em 2026-07-17 — nomes de branch já fechados, pra não precisar decidir
de novo na hora de gravar cada aula. **As branches abaixo são o PLANO — só são
criadas quando a aula correspondente for de fato produzida** (não existem ainda,
exceto a da 1.3).

O **Módulo 8 não tem branches** — é um estudo de caso anonimizado (documentário
técnico sobre uma plataforma real), não uma evolução direta do
`customer-support-lab`.

### Módulo 1 — Base determinística

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 1.3 — Laboratório: o chatbot determinístico | Estrutura inicial, FastAPI, HTML, máquina de estados, Docker e testes | `lesson/m01-a03-chatbot-deterministico` ✅ criada |

### Módulo 2 — Conversação e primeira geração

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 2.1 — O que existe por trás de um chat | Exposição e visualização do payload de mensagens | `lesson/m02-a01-payload-conversacao` ✅ criada |
| 2.3 — Persona não é fantasia | Definição de identidade, escopo e comportamento do assistente | `lesson/m02-a03-persona-assistente` ✅ criada |
| 2.5 — Resumo de conversa | Compactação e resumo incremental do histórico | `lesson/m02-a05-resumo-conversa` ✅ criada |
| 2.8 — Primeira evolução generativa | Entrada livre, classificação de intenção, geração e fallback determinístico (componente local didático, sem LLM real) | `lesson/m02-a08-primeira-evolucao-generativa` ✅ criada |

### Módulo 3 — Spec Driven Development e contexto

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 3.3 — SDD na prática com `tlc-spec-driven` | Instalação da skill e criação da Spec (retroativa) da evolução generativa | `lesson/m03-a03-sdd-tlc-spec-driven` ✅ criada |
| 3.4 — Anatomia de uma boa Spec | Refinamento da Spec, critérios de aceite, testes e evidências | `lesson/m03-a04-refinamento-spec` ✅ criada |
| 3.5 — Primeira LLM local com Ollama | Instalação, execução e primeira chamada via API — **não altera o repositório** | — (sem branch) |
| 3.6 — Hardware pra IA local: CPU, GPU, VRAM e memória unificada | Conceito com demonstrações — **não altera o repositório** | — (sem branch) |
| 3.7 — Modelos locais por tarefa: texto, embeddings e visão | Conceito com demonstrações — **não altera o repositório** | — (sem branch) |
| 3.8 — Contexto em camadas e primeira inferência real | Organização dos arquivos/fontes de contexto + primeira conexão real do chatbot com Ollama | `lesson/m03-a08-contexto-em-camadas` ✅ criada |
| 3.9 — Prompts como artefatos versionados | Extração dos prompts do código e versionamento | `lesson/m03-a09-prompts-versionados` |
| 3.10 — Montagem condicional de prompts | Condições determinísticas resolvidas antes da inferência | `lesson/m03-a10-prompts-condicionais` |
| 3.11 — Contexto como infraestrutura | Base inicial de conhecimento e fluxo de atualização de contexto (fecho do módulo) | `lesson/m03-a11-contexto-como-infraestrutura` |

### Módulo 4 — Runtime e múltiplos agentes

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 4.1 — Agente como entidade declarativa | Definição de agentes em JSON ou YAML | `lesson/m04-a01-agente-declarativo` |
| 4.3 — Etapas declarativas e DSL | Pipeline interno e elementos de execução | `lesson/m04-a03-etapas-declarativas` |
| 4.4 — Fail-fast para agentes | Validação das configurações no boot | `lesson/m04-a04-validacao-fail-fast` |
| 4.5 — Tipando o grafo de conversa | Validação de origens, destinos e transições | `lesson/m04-a05-grafo-tipado` |
| 4.6 — Vários agentes em uma entrada | Triagem seguida de financeiro ou suporte | `lesson/m04-a06-multiplos-agentes` |
| 4.7 — Controle de loops | Limites de transição e proteção contra ciclos | `lesson/m04-a07-controle-de-loops` |
| 4.8 — Handoff e especialização | Transferência entre agentes e encaminhamento humano | `lesson/m04-a08-handoff-agentes` |
| 4.9 — Recuperação e fallback | Redirecionamento após falhas | `lesson/m04-a09-recuperacao-fallback` |
| 4.10 — Primeiro ecossistema | Consolidação do runtime com agentes especializados | `lesson/m04-a10-primeiro-ecossistema` |

### Módulo 5 — Tools, Skills e capacidades

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 5.2 — Tool e function calling | Contrato e executor inicial de ferramentas | `lesson/m05-a02-function-calling` |
| 5.4 — Router após a ferramenta | Roteamento conforme o resultado da execução | `lesson/m05-a04-router-pos-tool` |
| 5.6 — Banco de dados com segurança | Consulta de pedidos com usuário somente leitura | `lesson/m05-a06-tool-consulta-pedido` |
| 5.7 — CLI e RTK | Execução controlada de comandos e compactação de saída | `lesson/m05-a07-cli-com-rtk` |
| 5.8 — Context7 | Consulta de documentação sob demanda | `lesson/m05-a08-context7` |
| 5.9 — Playwright | Testes de interface, screenshots e evidências | `lesson/m05-a09-playwright` |
| 5.10 — FFmpeg | Extração de áudio e frames | `lesson/m05-a10-ffmpeg` |
| 5.11 — Canal externo | Integração inicial com WhatsApp | `lesson/m05-a11-canal-whatsapp` |
| 5.12 — Agente capaz de agir | Consolidação das ferramentas e evidências | `lesson/m05-a12-agente-capaz-de-agir` |

### Módulo 6 — Evolução multimodal

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 6.1 — Do menu pra linguagem natural | Entrada natural preservando o menu como fallback | `lesson/m06-a01-linguagem-natural` |
| 6.2 — Small Talk | Tratamento barato de saudações e conversas simples | `lesson/m06-a02-small-talk` |
| 6.3 — Guard Rails | Classificação de escopo e políticas de recusa | `lesson/m06-a03-guard-rails` |
| 6.4 — FAQ e RAG | Ingestão, recuperação e respostas baseadas em evidências | `lesson/m06-a04-faq-rag` |
| 6.5 — Histórico e memória | Memória curta, resumo e fatos persistentes | `lesson/m06-a05-historico-memoria` |
| 6.6 — Áudio | Speech-to-Text e Text-to-Speech por adapters | `lesson/m06-a06-audio` |
| 6.7 — Imagem e documentos | Recebimento e análise de imagens e documentos | `lesson/m06-a07-imagem-documentos` |
| 6.8 — Vídeo | Transcrição, frames e resumo multimodal | `lesson/m06-a08-video` |
| 6.9 — O canal é uma porta | Mesmo motor atendendo HTML e WhatsApp | `lesson/m06-a09-canais-e-adapters` |
| 6.10 — Agentes especialistas | Triagem, financeiro, suporte, cancelamento e humano | `lesson/m06-a10-agentes-especialistas` |

### Módulo 7 — Arquitetura agnóstica

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 7.2 — Provider como detalhe | Interface comum e primeiro adapter de modelo | `lesson/m07-a02-provider-adapter` |
| 7.3 — Saída estruturada | Objetos Pydantic e validação das respostas | `lesson/m07-a03-saida-estruturada` |
| 7.4 — RAG fora do provedor | Separação da recuperação e do fornecedor da LLM | `lesson/m07-a04-rag-agnostico` |
| 7.5 — STT e TTS substituíveis | Portas e adapters de voz | `lesson/m07-a05-voz-agnostica` |
| 7.6 — Estratégia multimodelo | Roteamento conforme custo, risco e complexidade | `lesson/m07-a06-estrategia-multimodelo` |
| 7.7 — Troca prática de provedor | Execução do mesmo agente com dois provedores | `lesson/m07-a07-troca-de-provedor` |

### Módulo 9 — Qualidade e observabilidade

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 9.2 — Testes gerados por agentes | Ampliação dos testes e casos de borda | `lesson/m09-a02-testes-gerados` |
| 9.3 — Testes end-to-end | Docker, Playwright e evidências | `lesson/m09-a03-testes-end-to-end` |
| 9.4 — Sonar e segurança | Análise estática e Quality Gate | `lesson/m09-a04-sonar-seguranca` |
| 9.5 — Pull Request por agente | Geração do PR com testes, riscos e evidências | `lesson/m09-a05-pull-request-agente` |
| 9.6 — Duas observabilidades | Métricas operacionais e comportamentais | `lesson/m09-a06-observabilidade-dupla` |
| 9.7 — Tracing de agentes | Trace por conversa, agente e ferramenta | `lesson/m09-a07-tracing-agentes` |
| 9.8 — Prometheus e Grafana | Métricas, dashboards e alertas | `lesson/m09-a08-prometheus-grafana` |
| 9.9 — Avaliação contínua | Dataset, regressão e comparação de versões | `lesson/m09-a09-avaliacao-continua` |

### Módulo 10 — Memória e otimização

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 10.2 — AgentMemory | Memória persistente de experiências e decisões | `lesson/m10-a02-agent-memory` |
| 10.3 — Contexto em grafo | Entidades, relações e temporalidade | `lesson/m10-a03-contexto-em-grafo` |
| 10.4 — Graphify | Geração e consulta do grafo do repositório | `lesson/m10-a04-graphify` |
| 10.5 — SLMs | Modelo pequeno pra classificação ou roteamento | `lesson/m10-a05-slm` |
| 10.6 — Fine-tuning | Preparação e avaliação de uma versão especializada | `lesson/m10-a06-fine-tuning` |
| 10.8 — Engenharia híbrida | Consolidação de regras, RAG, modelos e ferramentas | `lesson/m10-a08-engenharia-hibrida` |

### Módulo 11 — Operação e entrega

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 11.1 — Do Jira ao Pull Request | Esteira completa orientada por tarefa | `lesson/m11-a01-jira-ao-pull-request` |
| 11.2 — Pipeline e deploy | CI, migração, deploy e rollback | `lesson/m11-a02-pipeline-deploy` |
| 11.3 — Observabilidade operacional | Consulta e correlação de logs | `lesson/m11-a03-observabilidade-operacional` |
| 11.4 — Paralelismo com controle | Worktrees e agentes trabalhando em paralelo | `lesson/m11-a04-paralelismo-controlado` |

### Módulo 12 — Consolidação

| Aula | Evolução do laboratório | Branch |
|---|---|---|
| 12.1 — Revisão do laboratório | Ajustes finais e documentação da evolução | `lesson/m12-a01-revisao-laboratorio` |
| 12.2 — Demonstração ponta a ponta | Fluxo completo do card até o PR | `lesson/m12-a02-demonstracao-ponta-a-ponta` |
| 12.3 — Nova capacidade | Criação completa de uma capacidade reutilizável | `lesson/m12-a03-nova-capacidade` |
| 12.4 — Avaliação arquitetural | Aplicação do checklist e correções encontradas | `lesson/m12-a04-avaliacao-arquitetural` |
