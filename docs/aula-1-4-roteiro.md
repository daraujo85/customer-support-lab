# Aula 1.4 — Do codador ao orquestrador

> ✅ PUBLICADA — vídeo gerado, legendas (CC) enviadas, lesson
> `7b851ae9-d198-48ce-9afd-a0b25cf291cc`. Áudio: `eng-sw-era-agents-m01-a04.mp3`.
> Terminal e conversa com o Claude Code gravados de verdade (host, shim
> `CLAUDE_SHIM_MODE=analysis` — texto determinístico, sem escrever nada) via
> `.pipeline/esa/m1a4-*.sh` + `render_host.sh`. Montagem em
> `.pipeline/build_esa_m1a4.py`.

```text
Branch: nenhuma
Base: main
Alteração no laboratório: nenhuma
Commit: nenhum
```

O laboratório é usado **apenas como objeto de análise** nesta aula. Nenhum
arquivo é criado, alterado ou commitado — o chatbot determinístico da Aula 1.3
permanece exatamente como está (4 testes, nenhum código de produção tocado).

> Correção de rota (2026-07-17): a primeira versão desta aula tentou justificar
> uma branch (`lesson/m01-a04-do-codador-ao-orquestrador`) adicionando um teste
> só pra ter algo pra commitar. Isso é pedagogicamente errado — branch não
> existe porque existe aula, existe porque existe mudança real no
> repositório. Esse teste e a branch foram revertidos. Ver
> `docs/workflow-git.md` para a regra corrigida.

## Estado inicial (o mesmo fim da Aula 1.3, sem mudanças)

```bash
cd ~/Desktop/gc/customer-support-lab
git status                                    # clean, branch main
docker compose run --rm app python -m pytest  # 4 passed
```

Nenhuma LLM, nenhum serviço externo, 4 testes passando, sessão em memória,
Docker Compose publicando `8010:8000`.

## O que o Claude Code faz nesta aula (tudo sem alterar nada)

1. **Pedido ruim** — "Melhore o chatbot." (interrompida antes de qualquer
   alteração; serve pra apontar ambiguidade, falta de critério de aceite,
   escopo indefinido).
2. **Pedido orientado** — leitura de `README.md`, `docs/architecture.md`,
   `app/main.py`, `app/chat/state.py`, `app/chat/flow.py` e dos testes, sem
   alterar nada, terminando num plano hipotético (nunca executado).
3. **Validação de compreensão** — perguntas sobre o código real (comportamento
   de opção inválida, o que acontece com sessões no restart do container, onde
   fica o menu, por que Redis ainda não entra). As respostas certas batem 1:1
   com o código:
   - opção inválida → `flow.py::handle_input`, ramo `MAIN_MENU`, mantém o
     estado e devolve `"Não entendi. " + menu_text()`;
   - restart do container → sessão é só `dict` em memória (não persiste),
     então reinicia zerada;
   - menu → `app/chat/flow.py`, lista `MAIN_MENU`;
   - Redis → não resolve nenhuma dor desta etapa (não há nada a persistir
     entre processos ainda).
4. **Comparação pedido vago x pedido contextualizado** — encerramento
   conceitual da aula: contexto → restringir espaço de solução → exigir plano
   → revisar → autorizar (hipotético) → decisão final do humano. Nada disso
   passa por um `git commit`.

## O que NÃO entra nesta aula

Nenhuma alteração de código, teste, configuração ou documentação do
laboratório — nem mesmo uma mudança "pequena e reversível" como um teste
extra. Se um dia a aula precisar de fato alterar o repositório, aí sim ela
ganha branch + tags, seguindo `docs/workflow-git.md`.

## Entrega da aula (pra narração)

O laboratório permanece **idêntico** ao fim da Aula 1.3. A entrega pedagógica
não é código novo — é o aluno entender como conduzir um agente sem "entregar o
volante": contexto → restringir o espaço de solução → exigir plano → revisar
→ autorizar a menor mudança → validar execução → decisão final do humano. A
demonstração acontece inteiramente na conversa com o Claude Code, sem tocar o
repositório.
