import pytest

from app.chat.generative import Intent
from app.chat.prompt_builder import PromptAssemblyError, build_task_instruction
from app.chat.prompt_loader import load_prompt_bundle

BUNDLE = load_prompt_bundle()


def test_suporte_tecnico_recebe_base_mais_bloco_tecnico():
    instruction = build_task_instruction(BUNDLE, Intent.SUPORTE_TECNICO)

    assert "A área já foi determinada pelo sistema como: suporte_tecnico." in instruction
    assert "orientação inicial segura e reversível" in instruction


def test_financeiro_recebe_base_mais_bloco_financeiro():
    instruction = build_task_instruction(BUNDLE, Intent.FINANCEIRO)

    assert "A área já foi determinada pelo sistema como: financeiro." in instruction
    assert "número do pedido ou da fatura" in instruction


def test_informacoes_conta_recebe_base_mais_bloco_de_conta():
    instruction = build_task_instruction(BUNDLE, Intent.INFORMACOES_CONTA)

    assert "A área já foi determinada pelo sistema como: informacoes_conta." in instruction
    assert "qual dado o usuário deseja consultar" in instruction


def test_bloco_tecnico_nao_vaza_pro_financeiro():
    instruction = build_task_instruction(BUNDLE, Intent.FINANCEIRO)

    assert "abra o equipamento" not in instruction


def test_bloco_financeiro_nao_vaza_pra_conta():
    instruction = build_task_instruction(BUNDLE, Intent.INFORMACOES_CONTA)

    assert "número do pedido ou da fatura" not in instruction


def test_intent_e_renderizado_no_template_base():
    instruction = build_task_instruction(BUNDLE, Intent.FINANCEIRO)

    assert "{intent}" not in instruction


def test_base_sempre_vem_antes_do_bloco_especifico():
    instruction = build_task_instruction(BUNDLE, Intent.SUPORTE_TECNICO)

    base_pos = instruction.index("TAREFA ATUAL")
    specific_pos = instruction.index("ORIENTAÇÕES DA ÁREA")

    assert base_pos < specific_pos


def test_unknown_e_rejeitado():
    with pytest.raises(PromptAssemblyError):
        build_task_instruction(BUNDLE, Intent.UNKNOWN)


def test_human_handoff_e_rejeitado():
    with pytest.raises(PromptAssemblyError):
        build_task_instruction(BUNDLE, Intent.HUMAN_HANDOFF)


def test_mesma_entrada_produz_montagem_identica():
    first = build_task_instruction(BUNDLE, Intent.FINANCEIRO)
    second = build_task_instruction(BUNDLE, Intent.FINANCEIRO)

    assert first == second
