from __future__ import annotations

import json
from typing import Any

from openai import OpenAIError

from app.agent.logger import log_step
from app.agent.tools import TOOLS_SCHEMA, buscar_regla_prd

# Baranda #3 · BUDGET · límite de iteraciones del loop
MAX_STEPS = 5
# Baranda #1 · SCOPE · definida en el SYSTEM_PROMPT
SYSTEM_PROMPT = (
    "Solo respondés sobre el PRD. Si te preguntan otra cosa, respondés 'fuera de alcance'. "
    "No ejecutás acciones destructivas y no inventás resultados. "
    "Operás siguiendo el patrón ReAct: pensás, decidís la próxima acción y usás la herramienta adecuada. "
    "Tu decisión debe devolverse únicamente como JSON válido, sin Markdown ni texto adicional, con este formato exacto: "
    '{"thought": "razonamiento breve", "action": "buscar_regla_prd" o "final", "action_input": {"termino": "texto a buscar"}}. '
    'Cuando action sea \'final\', action_input debe contener {"respuesta": "respuesta final fundamentada"}.'
)
ALLOWED_ACTIONS = {"buscar_regla_prd", "final"}


def _parse_model_decision(raw_response: str) -> tuple[str, str, dict[str, Any]]:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:  # pragma: no cover - defensive
        raise ValueError(f"El modelo no devolvió JSON válido: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("La respuesta del modelo debe ser un objeto JSON.")

    thought = payload.get("thought")
    action = payload.get("action")
    action_input = payload.get("action_input")

    if not isinstance(thought, str) or not thought.strip():
        raise ValueError("El campo 'thought' debe ser un texto no vacío.")
    if not isinstance(action, str) or not action.strip():
        raise ValueError("El campo 'action' debe ser un texto no vacío.")
    if not isinstance(action_input, dict):
        raise ValueError("El campo 'action_input' debe ser un objeto JSON.")

    normalized_action = action.strip().lower()
    if normalized_action in {"finish", "final"}:
        normalized_action = "final"
    elif normalized_action in {"search_prd", "buscar_regla_prd"}:
        normalized_action = "buscar_regla_prd"

    return thought, normalized_action, action_input


def run_agent(question: str, client) -> str:
    """Ejecuta un bucle ReAct orientado a responder sobre el PRD."""
    messages: list[dict[str, str]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, MAX_STEPS + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0,
                tools=TOOLS_SCHEMA,
            )
        except OpenAIError as exc:
            return f"Error: no se pudo consultar el LLM: {exc}"

        raw = response.choices[0].message.content
        if not isinstance(raw, str) or not raw.strip():
            return "Error: el modelo respondió vacío."

        try:
            _, action, action_input = _parse_model_decision(raw)
        except ValueError as exc:
            return f"Error: respuesta inválida del modelo: {exc}"

        if action not in ALLOWED_ACTIONS:
            return (
                f"Error: acción no permitida: '{action}'. Solo se permiten "
                "'buscar_regla_prd' y 'final'."
            )

        if action == "final":
            respuesta = action_input.get("respuesta")
            if respuesta is None:
                respuesta = action_input.get("answer")
            if not isinstance(respuesta, str) or not respuesta.strip():
                return "Error: la respuesta final del modelo está vacía."
            respuesta = respuesta.strip()
            return respuesta

        termino = action_input.get("termino")
        if not isinstance(termino, str):
            return "Error: buscar_regla_prd requiere el campo 'termino' con texto."

        observation = buscar_regla_prd(termino)
        log_step(step, "buscar_regla_prd", {"termino": termino}, observation)

        messages.append({"role": "assistant", "content": raw})
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return (
        "Error: se alcanzó el límite de pasos de 5 sin una respuesta final "
        "válida del modelo."
    )
