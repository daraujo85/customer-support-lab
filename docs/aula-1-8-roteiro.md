# Aula 1.8 — Prova e Reflexão do Módulo

```text
Usa o laboratório: sim
Altera código: não
Altera documentação: não
Branch: nenhuma
Commit: nenhum
Base: main
```

Fecha o Módulo 1: nenhuma funcionalidade nova, nenhuma branch, nenhum commit.
Valida o estado final (`git status` limpo + 8 testes), percorre 10 situações
de julgamento (não perguntas de decorar), compara os três papéis
(programador/engenheiro/orquestrador), revisita a evolução da Aula 1.6 como
prova de que entrega não é só funcionalidade visível, e fecha com um
exercício real no Claude Code em modo análise (nunca escreve nada):
avaliação de 10 perguntas, delegação de tarefa por risco, e identificação de
evolução desnecessária no momento atual do laboratório.

## Gráfico inserido (Situação 3 — "usar IA para programar")

A narração pergunta se usar IA pra escrever parte de uma funcionalidade
significa não saber programar (resposta: não — o que importa é como a
ferramenta foi usada). Logo depois dessa situação se resolver, o vídeo
insere um gráfico de barras com dados reais do **Stack Overflow 2025
Developer Survey** (`survey.stackoverflow.co/2025/ai`, 49k+ respondentes de
177 países, cada pergunta com base de ~31-34 mil respostas):

| Indicador                                     | % |
|------------------------------------------------|---|
| Usam ou planejam usar IA                        | 84 |
| Frustram-se com respostas quase certas          | 66 |
| Desconfiam da precisão                          | 46 |
| Gastam mais tempo depurando código de IA        | 45 |
| Confiam na precisão                             | 33 |

Título do gráfico: "Adoção alta, confiança baixa". Rodapé de metodologia:
métricas vêm de perguntas diferentes da pesquisa, não somam um mesmo total.

Implementado como `buildlib.g_bars(items, title=, footnote=)` — nova função
de gráfico (trilho escuro `#221f18`, barra em gradiente, label à direita,
percentual monoespaçado; item de menor destaque em lima `#c9e85a`), seguindo
o spec "Barra horizontal" já documentado em `.pipeline/DESIGN_SLIDES.md`.

## ✅ Publicado

Áudio transcrito (`segs_m1a8.json`, 319 segmentos, ~785s). 27 cues montados
em `build_esa_m1a8.py`. Clipes reais gravados (host, `GIT_PAGER=cat`):

- `m1a8-terminal-start` — `git status` + `docker compose run --rm app
  python -m pytest -v` (valida o estado final do módulo).
- `m1a8-claude-avaliacao` — shim `CLAUDE_SHIM_STEP=avaliacao_10_perguntas`
  (Claude Code lê README/docs/código/testes e prepara a avaliação).
- `m1a8-claude-delegacao` — shim `CLAUDE_SHIM_STEP=tarefa_baixo_risco`.
- `m1a8-claude-evolucao` — shim `CLAUDE_SHIM_STEP=evolucao_desnecessaria`.
- `m1a8-terminal-final` — `git status` limpo, fechamento.

Renderizado (24.3MB, ~785s), legendas via `transcript_tools.py cc-payload`,
upload + publish na lesson `24c27284-ebec-408b-8c85-9298583c2fc7`.
