# Aula 1.5 — Human in the Loop

```text
Branch: nenhuma
Base: main
Alteração no laboratório: nenhuma
Commit: nenhum
```

Igual à Aula 1.4: o laboratório é usado **só como objeto de análise**. O
Claude Code lê o repo real e propõe uma matriz de autonomia + um fluxo de
trabalho — nada é escrito no disco. Fonte: `.pipeline/esa/segs_m1a5.json`
(216 segmentos, ~684s).

## Estrutura da aula (da narração)

1. **Recapitulação da 1.4** (0–21s) — o que foi feito (leitura, validação,
   comparação de pedido vago x estruturado), sem imagem/clip novo — cabe num
   slide de recapitulação (`g_cards` ou `g_statement`).
2. **O que é Human in the Loop** (21–58s) — definição: não é aprovar cada
   clique (vira "estagiário com medo do bloco de notas" — ótima analogia de
   humor visual, dá imagem), é colocar aprovação nos pontos certos
   proporcional a impacto/risco/irreversibilidade/acesso externo.
3. **Terminal inicial** (58–90s) — `cd`, `git status` (limpo), `docker
   compose run pytest` (4 testes) — igual ao padrão da 1.4. Reaproveitar o
   clipe `m1a4-status.sh` adaptado (mesmo repo, mesmos comandos) ou gravar um
   novo `m1a5-status.sh` idêntico em estrutura.
4. **Instrução ao Claude Code — pedido de análise** (90–202s) — prompt real
   e extenso, ditado quase literalmente no áudio:
   > "Analise o repositório atual do Customer Support Lab como preparação
   > para uma aula sobre Human in the Loop. Leia o README.md,
   > docs/architecture.md, docs/course-roadmap.md, app/main.py,
   > app/chat/state.py, app/chat/flow.py, os arquivos da pasta app/static e
   > tests/test_chat_flow.py. Não altere nenhum arquivo. Não crie branch.
   > Não instale dependências. Não faça refatoração. Não faça commits.
   > Primeiro, explique resumidamente como o sistema funciona hoje. Depois,
   > classifique as ações possíveis em três níveis: Nível 1 (execução
   > autônoma permitida), Nível 2 (execução somente depois de aprovação
   > humana), Nível 3 (ação que deve continuar sob responsabilidade humana).
   > Para cada ação, informe o risco, a evidência que o agente precisa
   > apresentar e o ponto em que deve parar e pedir autorização. Considere:
   > leitura de arquivos, explicação da arquitetura, execução de testes,
   > criação de testes, alteração de resposta fixa, nova opção de menu,
   > mudança de estado, alteração do contrato da API, instalação de
   > dependência, adição de Redis, chamada de LLM, uso de credencial
   > externa, criação de commits, abertura de pull requests, merge e deploy.
   > No final, proponha um fluxo com objetivo, contexto, plano, aprovação,
   > execução, diff, testes, revisão, commit e pull request. Não implemente
   > nada. Confirme no final que nenhum arquivo foi modificado."
5. **Nível 1 — autonomia** (205–236s) — ler arquivos, explicar arquitetura,
   rodar testes, mostrar diff: reversível, mas SEMPRE com evidência (comando +
   resultado, não só afirmação).
6. **Nível 2 — aprovação prévia** (236–292s) — criar teste, alterar resposta
   fixa, nova opção de menu, mudar estado, instalar dependência: mexe no
   repo, exige plano (arquivos, motivo, risco, validação) antes de agir. Se o
   escopo crescer durante a implementação, para e pede nova aprovação —
   "uma aprovação não é um cheque em branco".
7. **Nível 3 — decisão humana permanente** (293–325s) — contrato de API,
   LLM nova, credencial externa, dados reais, permissões, deploy, merge,
   mudanças de segurança: o agente prepara (PR, riscos, evidências), mas
   quem decide é humano.
8. **Exemplo do laboratório: Redis** (325–362s) — sessão em memória é uma
   limitação conhecida; o agente pode identificar e até sugerir Redis, mas
   NÃO deve adicionar sozinho — falta responder se há dor real (sobreviver a
   reinício? múltiplas instâncias? escala? orçamento?). "O agente sugere. O
   engenheiro decide."
9. **Exemplo: mudar o texto da opção 4** (363–395s) — até uma frase pode ter
   impacto (promessa que a operação não cumpre, linguagem jurídica) — baixo
   risco aparente não é baixo risco real.
10. **Exemplo: nova opção de menu** (395–426s) — implementação é só parte da
    entrega; antes tem decisão de produto (que problema resolve, é estado
    novo ou variação, termina ou continua o atendimento, encaminhamento
    humano, comportamento de entrada inválida).
11. **Matriz de autonomia** (426–517s) — pedido ao Claude para apresentar a
    matriz (ação × nível × risco × evidência × ponto de aprovação), só na
    conversa, sem criar arquivo. 9 exemplos concretos narrados (ler main.py,
    rodar testes, criar teste, alterar resposta fixa, instalar dependência,
    chamar LLM, usar credencial, merge, deploy) — material perfeito pra um
    slide `g_cards`/tabela.
12. **Fluxo de 10 etapas** (517–591s) — objetivo → contexto → plano →
    aprovação → execução → diff → testes → revisão → commit → pull request.
    Merge fica de fora do fluxo do agente (política da equipe decide). Ótimo
    para `g_flow` ou `g_steps` (mas 10 itens — quebrar em 2 grupos de 5 pra
    não estourar o limite de ~4 por linha do `g_steps`/`g_flow`).
13. **Autonomia proporcional ao risco** (579–593s) — não faz sentido pedir
    aprovação pra ler um arquivo, nem dar a mesma liberdade de teste local
    pro deploy em produção.
14. **Análise final: pontos de parada obrigatória** (591–615s) — pedido final
    ao Claude: listar onde o agente DEVE parar (contrato de API, dependência
    nova, serviço externo, credencial, persistência, LLM, commit, PR, merge,
    deploy) + confirmação de que nada foi alterado.
15. **Terminal final** (615–632s) — `git status` limpo, sem branch, sem
    commit — igual ao encerramento da 1.4.
16. **Encerramento conceitual** (632–684s) — a entrega da aula é uma
    **política de decisão**, não código. Frase-âncora: "Quanto maior o poder
    do agente, mais claros precisam ser os limites e a responsabilidade
    humana." Preview da 1.6 (conectar com DDD, testes, Clean Architecture,
    DevOps, SDD).

## Shim — novo modo `CLAUDE_SHIM_MODE=analysis`, steps novos

Reaproveita o mecanismo já criado pra Aula 1.4 (`lib/shims/claude`), mas com
steps NOVOS específicos desta aula (não reaproveitar os steps de 1.4 —
conteúdo é outro):

- `sistema_resumo` — resumo curto de como o sistema funciona hoje (chatbot
  determinístico, 4 estados de atendimento, sessão em memória).
- `matriz_autonomia` — a matriz com os 9 exemplos narrados, 3 níveis.
- `fluxo_10_etapas` — as 10 etapas (objetivo → ... → pull request), com nota
  de que merge fica fora do fluxo do agente.
- `pontos_de_parada` — lista final de onde o agente deve parar
  obrigatoriamente + confirmação "nenhum arquivo foi modificado".

Cada step só imprime texto (nenhum `Write`, nenhum `mkdir` fora de tmp) —
mais simples que o modo `scaffold` da 1.3, no mesmo espírito do modo
`analysis` da 1.4.

## Clipes a gravar (host, real repo, mesmo padrão da 1.4)

| Clipe | Conteúdo |
|---|---|
| `m1a5-status.sh` | cd + git status + docker compose run pytest (4 passed) |
| `m1a5-claude-analise.sh` | prompt completo de análise (item 4 acima) + `sistema_resumo` |
| `m1a5-claude-matriz.sh` | pedido da matriz de autonomia + `matriz_autonomia` |
| `m1a5-claude-fluxo.sh` | pedido do fluxo de 10 etapas + `fluxo_10_etapas` |
| `m1a5-claude-parada.sh` | pedido dos pontos de parada + `pontos_de_parada` |
| `m1a5-status-final.sh` | git status limpo + git log (confirma nenhum commit) |

## Oportunidades de imagem Gemini (humor visual / analogia forte)

1. **"Estagiário com medo de abrir o bloco de notas"** (33–38s) — analogia
   cômica de excesso de aprovação — imagem de um estagiário hesitante diante
   de um notebook simples, ambiente de escritório.
2. **Nível 1/2/3 como semáforo de risco** — imagem conceitual opcional (três
   zonas de luz verde/amarelo/vermelho) pra abrir o bloco dos 3 níveis, ou
   manter só gráfico (mais alinhado ao `DESIGN_SLIDES.md`, evita clichê de
   semáforo se preferir).
3. **"O agente sugere, o engenheiro decide"** (Redis) — imagem de uma mão
   humana assinando/aprovando algo ao lado de uma sugestão técnica,
   reforçando autoridade final humana.

Duas a três imagens bastam (mesmo volume das aulas 1.3/1.4 depois do ajuste
recente) — o grosso da aula já tem variedade via matriz/fluxo em
`g_cards`/`g_flow`/`g_compare` (agora com o visual novo).

## Pendente pra produção (próximo passo, não incluído neste plano)

- Gerar as 2–3 imagens Gemini acima.
- Estender o shim com os 4 novos steps.
- Gravar os 6 clipes (host real, mesmo padrão de `render_host.sh`).
- Escrever `build_esa_m1a5.py` com os cues mapeados aos anchors do
  `segs_m1a5.json`.
- Renderizar, subir vídeo + CC, confirmar `isPublished` consistente com as
  demais aulas do módulo.
