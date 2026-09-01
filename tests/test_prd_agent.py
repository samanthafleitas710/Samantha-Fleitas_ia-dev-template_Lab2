from __future__ import annotations

from app.agent.loop import run_agent
from app.agent.tools import buscar_regla_prd
from tests.mocks.mock_llm import MockLLMClient, mock_chat_response


def test_buscar_regla_prd_returns_context_and_line_numbers() -> None:
    result = buscar_regla_prd("90 días")

    assert "línea" in result.lower()
    assert "90 días" in result.lower()
    assert "90" in result


def test_buscar_regla_prd_handles_empty_term() -> None:
    result = buscar_regla_prd("   ")

    assert "vacío" in result.lower()


def test_run_agent_react_loop_with_tool_and_final() -> None:
    client = MockLLMClient(
        responses=[
            mock_chat_response(
                thought="Necesito buscar la regla del PRD.",
                action="buscar_regla_prd",
                action_input={"termino": "90 días"},
            ),
            mock_chat_response(
                thought="Ya tengo la evidencia. Respondo.",
                action="final",
                action_input={
                    "respuesta": "La consulta aplica a transacciones dentro de los últimos 90 días."
                },
            ),
        ]
    )

    result = run_agent("¿Cuál es el rango de la consulta del historial?", client)

    assert "90 días" in result
    assert "transacciones" in result.lower()


def test_run_agent_rejects_invalid_action() -> None:
    client = MockLLMClient(
        responses=[
            mock_chat_response(
                thought="Voy a usar una acción prohibida.",
                action="inventado",
                action_input={"termino": "90 días"},
            )
        ]
    )

    result = run_agent("Pregunta al agente con acción inválida", client)

    assert "no permitida" in result.lower() or "inválida" in result.lower()
