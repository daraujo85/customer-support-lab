# Fluxo de git por aula — branch + tags

A partir da **Aula 1.4**, toda aula que alterar o laboratório segue este fluxo
(decidido pelo Diego em 2026-07-17). A Aula 1.3 foi commitada direto na `main`
(antes deste padrão existir) — o fim dela ficou marcado retroativamente com a tag
`m01-a03-end`, sem uma tag `-start` correspondente (o repo nasceu já com o
baseline completo, não há um "antes" pra marcar sem reescrever histórico).

## Por que branch + tag, não só branch solta

Uma branch por aula sem merge na `main` faz o laboratório divergir — cada aula
vira uma ilha e o projeto deixa de contar uma história contínua. O fluxo certo:

```
main
 └── lesson/m01-a04-do-codador-ao-orquestrador
       └── merge (--no-ff) em main
 └── lesson/m02-a08-primeira-evolucao-generativa
       └── merge (--no-ff) em main
```

A `main` sempre representa a evolução OFICIAL do laboratório. As tags marcam os
checkpoints exatos usados na gravação — elas não mudam nunca (branch pode receber
commit novo ou ser apagada depois do merge; a tag não).

## Passo a passo por aula

**1. Antes de gravar** — marca o estado inicial e abre a branch:

```bash
git checkout main && git pull
git tag m01-a04-start
git checkout -b lesson/m01-a04-do-codador-ao-orquestrador
```

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
git merge --no-ff lesson/m01-a04-do-codador-ao-orquestrador
git tag m01-a04-end
git push origin main --tags
```

## Convenção de nomes

Branch: `lesson/<módulo>-<aula>-<slug-curto-do-tema>`
```
lesson/m01-a03-chatbot-deterministico
lesson/m01-a04-do-codador-ao-orquestrador
lesson/m02-a08-primeira-evolucao-generativa
lesson/m03-a03-sdd-com-tlc-spec-driven
```

Tags: `m<módulo com 2 dígitos>-a<aula com 2 dígitos>-start` / `-end`
```
m01-a03-start / m01-a03-end
m01-a04-start / m01-a04-end
```

## Comandos úteis

Comparar o que uma aula mudou:
```bash
git diff m01-a04-start m01-a04-end
```

Voltar pro estado exato de antes de uma aula (ex.: pra regravar):
```bash
git checkout m01-a04-start
```
