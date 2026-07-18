# Aula 1.7 — O próprio curso como prova do método

```text
Usa o laboratório: sim
Altera código: não
Altera documentação: não
Branch: nenhuma
Commit: nenhum
Base: main
```

Diferente das aulas 1.4/1.5 (o laboratório é objeto de análise) e da 1.6 (o
laboratório evolui de verdade), a 1.7 é uma **demonstração da esteira de
produção já usada**: mostra o histórico real — branch, tags, commits, testes,
diffs, docs — como prova de que o curso e o laboratório foram construídos com
o mesmo método que está sendo ensinado. Nada de novo é escrito; a árvore
começa e termina limpa.

## Tese da aula

> O curso não está apenas ensinando um método. O próprio curso e o
> laboratório foram produzidos usando esse método.

## O que a demonstração mostra (histórico real, sem alterar nada)

```bash
git log --oneline --graph --decorate --all
git tag --list "m01-*"
git diff m01-a06-start m01-a06-end
docker compose run --rm app python -m pytest
```

E os documentos que registram o processo, aula a aula:

```text
docs/tts-context.md
docs/workflow-git.md
docs/aula-1-3-roteiro.md
docs/aula-1-4-roteiro.md
docs/aula-1-5-roteiro.md
docs/aula-1-6-roteiro.md
```

## Pontos que a narração deve cobrir

- Evolução incremental entre aulas (1.3 → 1.6), nunca um salto.
- Diferença entre aula conceitual (1.1, 1.2), aula de leitura/análise (1.4,
  1.5) e aula de evolução prática (1.3, 1.6) — a regra fundamental do
  `workflow-git.md`: branch existe por mudança real, não por aula existir.
- Tags de início e fim marcando o checkpoint exato de cada evolução
  (`m01-a03-end`, `m01-a06-start`/`-end`).
- Commits pequenos e intencionais (a 1.6 teve 3: caracterizar → refatorar →
  ampliar cobertura) — nunca um commit gigante no final.
- Testes como evidência, não afirmação — sempre rodados dentro do container
  (`docker compose run --rm app python -m pytest`), nunca só "funciona aqui".
- Revisão do diff antes do merge; merge sempre `--no-ff` na `main`.
- Documentação do contexto (`tts-context.md`) e do roteiro de cada aula
  (`aula-1-X-roteiro.md`) — o processo de produção do CURSO em si também
  segue o método (ler antes de escrever, registrar decisões, nada de "confia
  em mim").

## Clipes previstos (a definir com o áudio real)

Prováveis candidatos, todos com comandos **reais** (sem shim — é histórico
genuíno, mesmo padrão da 1.6):

- Terminal: `git log --oneline --graph --decorate --all` (visão geral do
  histórico do repo inteiro).
- Terminal: `git tag --list "m01-*"` (todas as tags do módulo 1 até aqui).
- Terminal: `git diff m01-a06-start m01-a06-end` (reaproveita o mesmo diff já
  usado na 1.6, agora como prova/exemplo, não como novidade).
- Terminal: `docker compose run --rm app python -m pytest` (evidência viva).
- Editor (`base`, nunca `typed`): abrir `docs/workflow-git.md` e/ou
  `docs/tts-context.md` mostrando a documentação real já existente.

Igual às aulas 1.4/1.5/1.6: **nenhum shim de escrita é necessário aqui** — é
tudo leitura de histórico e arquivos que já existem, sem Claude Code
envolvido em nenhum ponto (não há pedido de análise nem implementação nesta
aula, só demonstração direta do que já está no repo).

## ✅ Publicado

Áudio transcrito (`segs_m1a7.json`, 253 segmentos, ~830s). 31 cues montados
em `build_esa_m1a7.py`, todos casados com âncoras reais da narração. Clipes
gravados (real, host, mesmo padrão da 1.6 — `GIT_PAGER=cat`/`--no-pager`
aplicado em todo comando de log/diff):

- `m1a7-terminal-log` — `git status` · `fetch --all --tags` ·
  `log --oneline --graph --decorate --all` · `tag --list "m01-*"`.
- `m1a7-editor-workflow` / `-tts` / `-roadmap` / `-architecture` /
  `-roteiros` — abre cada doc real (`base`, sem `typed`).
- `m1a7-claude-analise` — shim `CLAUDE_SHIM_MODE=analysis
  CLAUDE_SHIM_STEP=analisa_esteira`.
- `m1a7-claude-metodo` — shim `CLAUDE_SHIM_STEP=metodo_9_etapas`.
- `m1a7-terminal-diffs` — `log m01-a06-start..end --no-merges` · `diff`
  completo.
- `m1a7-terminal-pytest` — `docker compose run --rm app python -m pytest -v`
  (8 testes).
- `m1a7-terminal-up` + `m1a7-browser-app` (captura real via `capweb.js` em
  `localhost:8010`) + `m1a7-terminal-down`.
- `m1a7-claude-final` — shim `CLAUDE_SHIM_STEP=conteudo_vs_evidencia`.
- `m1a7-terminal-final` — `git status` limpo, fechamento.

Renderizado (32.6MB, ~830s), legendas geradas via
`transcript_tools.py cc-payload`, upload + publish na lesson
`074aa0a7-9457-4b1e-b317-54983ca1e9bc`.
