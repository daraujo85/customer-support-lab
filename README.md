# Customer Support Lab

Laboratório evolutivo do curso [**Engenharia de Software na Era dos Agentes**](https://garagemdocodigo.com.br) — começa como um chatbot determinístico e evolui, aula a aula, até um ecossistema de agentes multimodal.

Domínio fictício (atendimento ao cliente genérico) — sem dado real de clientes ou negócio.

## Rodando

```bash
docker compose up --build
```

Depois abra `http://localhost:8010` no navegador.

Nenhuma instalação de Python ou dependência é necessária na sua máquina — tudo roda
dentro do container.

## Rodando os testes

```bash
docker compose run --rm app python -m pytest
```

## Estrutura

```
app/
  main.py          # FastAPI: serve a página + POST /api/chat
  chat/
    flow.py         # árvore de decisão determinística
    state.py        # estados, eventos e sessão
  static/           # HTML/CSS/JS do widget de chat
tests/              # pytest
docs/               # arquitetura + roadmap do laboratório por módulo
specs/              # Specs produzidas com a skill tlc-spec-driven (a partir do Módulo 3)
skills/             # skills/playbooks do curso
```

## Estado atual

**Aula 3.4** — refinamento da Spec criada na 3.3: o mesmo arquivo
(`specs/m02-a08-primeira-evolucao-generativa/spec.md`) ganhou critérios de
aceite numerados, observáveis e binários (AC-01 a AC-08) e uma matriz de
rastreabilidade explícita ligando cada critério ao(s) teste(s) que o
comprovam. Nenhum código de aplicação ou teste mudou — só documentação. Ver
`docs/architecture.md` para a evolução planejada módulo a módulo.
