# Aula 1.4 — Do codador ao orquestrador

> ✅ Implementado e registrado no repo (branch mergeada, tags criadas). Esta
> aula **não é uma evolução funcional** do laboratório — é uma demonstração de
> postura de condução de um agente de código, usando o chatbot já pronto da
> Aula 1.3.

## Estado inicial (o mesmo fim da Aula 1.3)

```bash
cd ~/Desktop/gc/customer-support-lab
git status                                    # clean, branch main
docker compose run --rm app python -m pytest  # 4 passed
```

Nenhuma LLM, nenhum serviço externo, 4 testes passando, sessão em memória,
Docker Compose publicando `8010:8000`.

## As quatro demonstrações do roteiro (conceituais, sem lab)

1. **Pedido ruim** — "Melhore o chatbot." (interrompida antes de qualquer
   alteração; serve pra apontar ambiguidade, falta de critério de aceite,
   escopo indefinido).
2. **Pedido orientado** — leitura de `README.md`, `docs/architecture.md`,
   `app/main.py`, `app/chat/state.py`, `app/chat/flow.py` e dos testes, sem
   alterar nada, terminando em um plano.
3. **Validação de compreensão** — perguntas sobre o código real (comportamento
   de opção inválida, o que acontece com sessões no restart do container, onde
   fica o menu, por que Redis ainda não entra). As respostas certas batem 1:1
   com o código:
   - opção inválida → `flow.py::handle_input`, ramo `MAIN_MENU`, mantém o
     estado e devolve `"Não entendi. " + menu_text()`;
   - restart do container → sessão é só `dict` em memória em `main.py` (não
     documentado neste arquivo, mas é a estrutura real), então reinicia zerada;
   - menu → `app/chat/flow.py`, lista `MAIN_MENU`;
   - Redis → não resolve nenhuma dor desta etapa (não há nada a persistir
     entre processos ainda).
4. **Tarefa controlada** — a única mudança real desta aula (ver abaixo).

## O que foi de fato implementado

O comportamento de encerramento **já existia** em `app/chat/flow.py::handle_input`:
qualquer estado que não seja `GREETING` nem `MAIN_MENU` move a sessão pra
`ChatState.ENCERRADO` e devolve a mensagem de agradecimento — mas não havia
teste cobrindo isso.

Prompt usado (conduzido, não "faz aí"):
```text
Com base na leitura anterior, proponha um teste para o comportamento de
encerramento. Não altere o código de produção. Adicione somente o menor
teste necessário em tests/test_chat_flow.py. Depois execute a suíte completa
e mostre o diff. Não faça commit.
```

Teste adicionado em `tests/test_chat_flow.py`:
```python
def test_new_message_in_final_state_closes_the_session():
    session = Session(state=ChatState.SUPORTE_TECNICO)
    reply = handle_input(session, "obrigado, resolvido")

    assert session.state == ChatState.ENCERRADO
    assert "Obrigado pelo contato" in reply
```

Validação (precisa de `docker compose build app` antes — a imagem já buildada
não pega arquivo novo sem rebuild):
```bash
docker compose build app
docker compose run --rm app python -m pytest -v
# 5 passed in 0.01s (as 4 anteriores + a nova)
```

`git diff --stat` mostrou **só** `tests/test_chat_flow.py | 8 ++++++++` — nenhum
arquivo de produção mudou. Nenhum risco: teste só exercita um caminho já
existente do código.

## Decisão tomada: opção recomendada (manter o teste)

Foi commitado, não descartado — o comportamento é real e já existia, então a
cobertura tem valor permanente.

```bash
git checkout main && git pull
git tag m01-a04-start
git checkout -b lesson/m01-a04-do-codador-ao-orquestrador

# edição do teste

docker compose build app
docker compose run --rm app python -m pytest -v   # 5 passed

git add tests/test_chat_flow.py
git commit -m "test: cobre encerramento do fluxo determinístico"

git checkout main
git merge --no-ff lesson/m01-a04-do-codador-ao-orquestrador
git tag m01-a04-end
git push origin main --tags
```

Estado final: `main` com 5 testes passando, branch
`lesson/m01-a04-do-codador-ao-orquestrador` mergeada, tags `m01-a04-start` e
`m01-a04-end` publicadas.

## O que NÃO entrou nesta aula

LLM, entrada em linguagem natural, novos estados, banco de dados, Redis,
persistência, agentes declarativos, Specs, Skills, refatoração ampla,
alteração de interface — tudo isso fica pras aulas seguintes (a próxima
evolução funcional real do laboratório é a 2.1, conforme
`docs/workflow-git.md`).

## Entrega da aula (pra narração)

O laboratório permanece **funcionalmente igual** ao fim da Aula 1.3, ganhando
apenas um teste. A entrega pedagógica não é código novo — é o aluno entender
como conduzir um agente sem "entregar o volante": contexto → restringir o
espaço de solução → exigir plano → revisar → autorizar a menor mudança →
validar execução → decisão final do humano.
