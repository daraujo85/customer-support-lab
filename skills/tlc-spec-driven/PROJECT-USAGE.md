# Uso desta skill neste projeto

Esta pasta é uma cópia local e versionada da skill "Tech Lead's Club -
Spec-Driven Development", instalada aqui a partir da Aula 3.3 do curso
"Engenharia de Software na Era dos Agentes".

- **Autoria**: Felipe Rodrigues — github.com/felipfr
- **Licença**: CC-BY-4.0
- **Versão copiada**: 2.0.0
- **Origem**: `~/.claude/skills/tlc-spec-driven` (instalação global do instrutor)
- **Data da cópia**: 2026-07-21

## Por que uma cópia local, não um link nem uma menção no README

Se a skill existisse só na máquina pessoal do instrutor, o repositório não
registraria qual versão foi usada — outra pessoa clonando o projeto poderia
não ter a skill, ou ter uma versão diferente, e o mesmo pedido seguiria um
processo diferente. Um atalho/link simbólico pra pasta global quebraria em
qualquer outra máquina. Por isso a skill inteira é copiada e comitada aqui,
sem editar nenhum arquivo original.

## Regras deste projeto

- **Não atualizar silenciosamente.** Se uma versão nova da skill for
  incorporada no futuro, isso deve ser uma decisão explícita, registrada em
  commit próprio — nunca uma sobrescrita despercebida.
- **Destino dos artefatos**: os documentos gerados pela skill (Spec, Design,
  Tasks) vão sempre em `specs/`, na raiz do projeto — visível, não escondida.
  Não criar uma segunda árvore paralela (ex.: `.specs/`) com o mesmo propósito.
- Os arquivos originais desta pasta (`SKILL.md`, `README.md`, `references/`)
  não são editados — qualquer ajuste de convenção do curso fica registrado
  aqui neste `PROJECT-USAGE.md`, nunca dentro da skill original.
