# Aula 1.6 — Fundamentos que permanecem (DDD, testes, arquitetura, DevOps, SDD)

> ✅ PUBLICADA — vídeo gerado (21/21 cues, ~775s), legendas (CC) enviadas,
> lesson `9ae828ad-b306-4383-a7c4-7b21b301a4d4`. Áudio:
> `eng-sw-era-agents-m01-a06.mp3`. Diferente das aulas 1.4/1.5, esta aula
> **tem evolução real no laboratório** — pequena, protegida por testes, sem
> funcionalidade nova. O vídeo inspeciona o histórico JÁ EXISTENTE (git
> switch --detach entre as tags, git log, git diff reais), não finge criar
> nada ao vivo. 6 clipes reais (host) via `.pipeline/esa/m1a6-*.sh` +
> `render_host.sh`; 2 deles usam o shim do Claude Code
> (`CLAUDE_SHIM_MODE=analysis`, steps `regra_de_negocio` e `compara_tags`) —
> os outros 4 são comandos git/docker 100% reais, sem shim nenhum. Montagem
> em `.pipeline/build_esa_m1a6.py`.
>
> ⚠️ Armadilha encontrada na gravação: `git log`/`git diff` sem
> `--no-pager` abrem `less` e travam pra sempre num terminal não-interativo
> (ficou preso ~1h46 até eu perceber e matar o processo). Fix: exportar
> `GIT_PAGER=cat` e usar `git --no-pager <comando>` em todo script de
> terminal real que rodar `log`/`diff`/`show`. Também usei `--no-merges` no
> `git log start..end` pra bater com "os três commits reais" da narração
> (sem isso, o merge commit aparece como um 4º item).

```text
Branch: lesson/m01-a06-fundamentos-engenharia
Base: main (pós Aula 1.3 — 1.4 e 1.5 não alteraram o repo)
Alteração no laboratório: refatoração de domínio + testes
Commit: 3 commits pequenos, mergeados --no-ff na main
```

## Objetivo prático

Refatorar a resolução da opção do menu — hoje embutida dentro de
`handle_input` como uma busca inline (`next((o for o in MAIN_MENU if o.key ==
user_input), None)`) — para uma função de domínio explícita
`resolve_menu_option`, sem alterar nenhum comportamento externo do chatbot.

## O que foi alterado (só isto)

```text
app/chat/flow.py
tests/test_chat_flow.py
```

Confirmado via `git diff --stat main` antes do merge: `app/main.py`,
`app/static/*`, `docker-compose.yml` e `pyproject.toml` **não** mudaram uma
linha. Nenhuma dependência foi instalada.

## As 3 etapas reais (3 commits)

**1. `test: caracteriza o encerramento após opção selecionada`**
```python
def test_message_after_selected_option_ends_conversation():
    session = Session(state=ChatState.SUPORTE_TECNICO)

    reply = handle_input(session, "Meu computador não liga")

    assert session.state == ChatState.ENCERRADO
    assert "Obrigado pelo contato" in reply
```
Teste de caracterização: registra um comportamento que já existia (qualquer
mensagem fora de `GREETING`/`MAIN_MENU` encerra a sessão) ANTES de mexer na
estrutura — 5 testes passando neste ponto.

**2. `refactor: extrai resolve_menu_option como regra de domínio explícita`**
```python
def resolve_menu_option(user_input: str) -> MenuOption | None:
    normalized_input = user_input.strip()
    return next(
        (option for option in MAIN_MENU if option.key == normalized_input),
        None,
    )
```
`handle_input` passou a chamar `resolve_menu_option(user_input)` em vez da
busca inline. Zero mudança de comportamento — só estrutura. 5 testes
continuam passando (nenhuma regressão).

**3. `test: cobre resolve_menu_option (válida, espaços, inexistente)`**
```python
def test_resolve_menu_option_returns_expected_option(): ...   # "1" -> Suporte técnico
def test_resolve_menu_option_ignores_surrounding_spaces(): ... # " 1 " -> mesma opção
def test_resolve_menu_option_returns_none_for_unknown_option(): ... # "9" -> None
```
Suíte final: **8 testes passando** (4 originais da 1.3 + 4 novos desta aula).

## Validação (real, rodada a cada etapa)

```bash
docker compose build app
docker compose run --rm app python -m pytest -v
```

## Fluxo git usado

```bash
git checkout main && git pull
git tag m01-a06-start
git checkout -b lesson/m01-a06-fundamentos-engenharia
# 3 commits pequenos (acima)
git checkout main
git merge --no-ff lesson/m01-a06-fundamentos-engenharia
git tag m01-a06-end
git push origin main --tags
```

## Como isso conecta os fundamentos (pra narração)

- **DDD** — `resolve_menu_option` dá nome explícito a uma regra do domínio
  que antes era só uma busca numa lista. `ChatState`/`MenuOption`/`Session`
  já eram a linguagem de domínio inicial (Aula 1.3); esta aula reforça o
  padrão.
- **Testes** — ordem real foi: caracterizar o comportamento existente →
  refatorar a estrutura → testar a regra isolada. A suíte prova que a
  refatoração não mudou transições, respostas, entrada inválida nem
  encerramento.
- **Arquitetura limpa** — a regra continua dentro de `app/chat`, sem
  depender de FastAPI/HTML/JS/Docker. O núcleo é testável sem subir servidor.
- **DevOps** — validação sempre rodou dentro do container
  (`docker compose run --rm app python -m pytest`), nunca "funciona na minha
  máquina".
- **Spec Driven Development** — a aula NÃO instala nem usa a skill
  `tlc-spec-driven` (isso é Módulo 3), mas já introduz o raciocínio de
  objetivo/restrições/critérios de aceite antes de codificar, sem antecipar
  a ferramenta formal.

## Entrega da aula (pra narração)

> O comportamento não mudou, mas a engenharia melhorou.

O laboratório evolui de forma pequena e sem risco: mesma API, mesma
interface, mesmas respostas — só a estrutura interna ficou mais clara e
melhor testada.
