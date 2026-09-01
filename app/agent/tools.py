from __future__ import annotations

from pathlib import Path

PRD_PATH = Path(__file__).resolve().parents[2] / "docs" / "prd" / "PRD.md"

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "buscar_regla_prd",
            "description": (
                "Busca un término dentro del PRD de LegacyPay y devuelve coincidencias "
                "con contexto y números de línea."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "Término a buscar en el PRD.",
                    }
                },
                "required": ["termino"],
            },
        },
    }
]


def buscar_regla_prd(termino: str) -> str:
    """Busca un término en el PRD con hasta 3 líneas de contexto antes y después."""
    if termino is None or not str(termino).strip():
        return "Error: el término de búsqueda está vacío."

    if not PRD_PATH.exists():
        return f"Error: no se encontró el PRD en {PRD_PATH}."

    term = str(termino).strip()
    lines = PRD_PATH.read_text(encoding="utf-8").splitlines()
    matches: list[str] = []

    for index, line in enumerate(lines):
        if term.lower() in line.lower():
            start = max(0, index - 3)
            end = min(len(lines), index + 4)

            context_lines = [
                f"Línea {line_index + 1}: {lines[line_index].rstrip()}"
                for line_index in range(start, end)
            ]

            matches.append("\n".join(context_lines))
            if len(matches) >= 3:
                break

    if not matches:
        return f"Sin coincidencias para '{term}' en el PRD."

    return "\n\n---\n\n".join(matches)
