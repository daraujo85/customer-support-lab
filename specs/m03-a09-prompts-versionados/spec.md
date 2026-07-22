# Spec — Prompts como artefatos versionados

> **Status: `prospectiva`** (mesma convenção da 3.8): escrita ANTES da
> implementação, autorizando e delimitando a mudança.

## Contexto e problema

Desde a Aula 3.8, a instrução de tarefa enviada ao Ollama
(`_TASK_INSTRUCTION_TEMPLATE`) vive como uma constante Python dentro de
`app/chat/ollama_generation.py` — de propósito, como dívida pedagógica
anotada na Spec da 3.8. Essa dívida cobra o preço de sempre: mudar o texto
do prompt exige mexer em código Python, o diff mistura lógica com redação,
e o histórico de revisão do prompt fica diluído no histórico geral do
arquivo.

## Objetivo

Extrair a instrução de tarefa para `prompts/task_instruction.md` — um
artefato Markdown versionado no git, revisável por Pull Request, com
histórico e diff próprios — sem mudar UMA VÍRGULA do texto nem do
comportamento observável da aplicação.

**Frase-guia:** o prompt não é uma string auxiliar escondida no código.
É um artefato de comportamento, com histórico, revisão, testes e rollback.

## Escopo

**Dentro do escopo:**
- Novo arquivo `prompts/task_instruction.md`, com o MESMO texto que hoje é
  a constante Python (incluindo o placeholder `{intent}`).
- Novo módulo `app/chat/prompt_loader.py` — `load_prompt_template()` lê e
  VALIDA o arquivo (existe, UTF-8 válido, não vazio, declara `{intent}`,
  não declara placeholders desconhecidos). Só lê e valida; não decide
  quando carregar nem como renderizar.
- `OllamaGenerativeComponent` passa a RECEBER o template já carregado via
  construtor (`task_instruction_template`) — deixa de conhecer caminho de
  arquivo. `_add_task_instruction` passa a receber o template como
  parâmetro.
- `app/main.py` (ponto de composição da aplicação) chama
  `load_prompt_template()` ANTES de construir o componente, só no modo
  `ollama`.
- `Dockerfile` copia `prompts/` pra dentro da imagem — sem isso o arquivo
  existiria no repositório mas desapareceria no container.
- Fail-fast: `GENERATION_MODE=ollama` com artefato ausente/vazio/inválido
  derruba o BOOT da aplicação. `local_didactic` e `disabled` não dependem
  do arquivo.
- Revisão real por Pull Request no GitHub (branch → PR → review → merge),
  como parte da demonstração da aula.

**Fora do escopo (explicitamente, decisão futura):**
- Mudar o TEXTO do prompt.
- Adicionar condições diferentes por intenção (fica pra 3.10 — montagem
  condicional de prompts).
- XML em runtime (o texto é predominantemente textual/linear; XML seria
  cerimônia sem resolver um problema real aqui — cabe quando for preciso
  delimitar conteúdo dinâmico/não confiável, ex. documento do usuário).
- Múltiplos templates, seleção dinâmica de prompt, hot reload.
- Buscar prompt em banco de dados ou interface administrativa.
- Versionamento semântico interno do arquivo (`version: 1` dentro do
  Markdown criaria uma segunda fonte de versionamento — a versão já é o
  histórico do git/commit/PR/tag da aula).
- Mudar classificação de intenção, score ou fallback.

## Requisitos funcionais

1. O texto da instrução de tarefa não existe mais como constante em
   `ollama_generation.py`.
2. O template oficial vive em `prompts/task_instruction.md`.
3. `load_prompt_template()` valida: arquivo existe, UTF-8 válido, não
   vazio, contém `{intent}`, não contém placeholders desconhecidos.
4. A renderização do template com uma intenção conhecida é IDÊNTICA à
   versão embutida da Aula 3.8 (mesmo texto, byte a byte).
5. `GENERATION_MODE=ollama` com o arquivo ausente ou inválido falha no
   boot (`PromptTemplateError`), antes de qualquer request HTTP.
6. `local_didactic` e `disabled` sobem normalmente mesmo se o arquivo de
   prompt estiver ausente/inválido — não dependem dele.
7. A instrução de tarefa continua entrando ANTES da última mensagem do
   usuário, nunca depois (correção descoberta na 3.8, preservada).
8. A imagem Docker contém o artefato de prompt.
9. Nenhum teste acessa rede real.
10. A alteração é revisada e mesclada via Pull Request real no GitHub.

## Restrições e invariantes (o que continua igual)

- Classificação de intenção, score, `MIN_ACCEPTED_SCORE=0,70`, transição
  de estado e fallback determinístico continuam exatamente como na 3.8.
- `docker-compose.yml`, `app/chat/flow.py`, `app/chat/generative.py` e
  `app/chat/summary.py` não mudam.
- Opções de geração (`temperature=0`, `seed=42`, `stream=false`) não
  mudam.
- Sem health-check do Ollama no boot — essa regra da 3.8 continua valendo
  (é uma falha de serviço externo, distinta da falha de configuração
  interna que esta aula introduz).

## Riscos e limitações

- **Risco aceito conscientemente**: separar prompt e código em arquivos
  diferentes significa que uma mudança de comportamento agora pode vir de
  DOIS lugares — o texto do prompt e a lógica que o usa. O Pull Request
  e a checklist de revisão (ver evidências) existem exatamente para
  mitigar isso.
- **Fora do escopo, não um bug**: sem montagem condicional, sem múltiplos
  templates — isso é a dor pedagógica da próxima aula (3.10).

## Evidências esperadas (a preencher depois da implementação)

- `tests/test_prompt_loader.py`: carrega o artefato oficial, contém
  `{intent}` e as regras de segurança, renderização idêntica à versão
  embutida da 3.8, erros claros para arquivo ausente/vazio/sem
  placeholder/placeholder desconhecido/UTF-8 inválido.
- `tests/test_ollama_generation.py`: atualizado para injetar o template
  via construtor; preserva o teste de ordem das mensagens (instrução
  antes da última mensagem).
- `tests/test_main_generation_mode.py`: modo `ollama` falha rápido quando
  o prompt é inválido; `local_didactic`/`disabled` não dependem do
  artefato.
- Suíte completa passando.
- Pull Request real aberto, revisado (comentário apontando pra uma regra
  de segurança específica) e mesclado no GitHub.

## Tags desta evolução

Branch `lesson/m03-a09-prompts-versionados`, tags `m03-a09-start` →
`m03-a09-end`, a partir do fim da Aula 3.8 (`m03-a08-end`/merge em
`main`).
