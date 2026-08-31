from __future__ import annotations

import socket
import subprocess
import sys
import time
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agent.loop import run_agent

MOCK_BASE_URL = "http://localhost:8001/v1"


def ensure_mock_llm_running() -> None:
    """Asegura que el mock de OpenAI esté levantado en localhost:8001."""
    try:
        with socket.create_connection(("127.0.0.1", 8001), timeout=0.5):
            return
    except OSError:
        pass

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.mock_llm:mock_app",
            "--host",
            "127.0.0.1",
            "--port",
            "8001",
        ],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    deadline = time.time() + 20
    while time.time() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", 8001), timeout=0.5):
                return
        except OSError:
            time.sleep(0.2)

    raise RuntimeError("No se pudo levantar el mock LLM en http://localhost:8001")


def make_client() -> OpenAI:
    return OpenAI(base_url=MOCK_BASE_URL, api_key="sk-mock")


def run_case(case_id: str, question: str, expected_phrase: str) -> bool:
    client = make_client()
    result = run_agent(question, client)
    ok = expected_phrase.lower() in result.lower()
    status = "✅" if ok else "❌"
    print(f"{status} {case_id}: {question}")
    print(f"   Resultado: {result}")
    print(f"   Esperado contiene: {expected_phrase}")
    return ok


if __name__ == "__main__":
    ensure_mock_llm_running()

    cases = [
        {
            "id": "rango-90-dias",
            "question": "¿cuál es el rango máximo del historial?",
            "expected": "90 días",
        },
        {
            "id": "pan-solo-ultimos-4",
            "question": "¿puedo exponer el PAN completo?",
            "expected": "últimos 4",
        },
        {
            "id": "fuera-de-alcance",
            "question": "¿cuál es la capital de Francia?",
            "expected": "Sin coincidencias",
        },
    ]

    passed = 0
    for case in cases:
        if run_case(case["id"], case["question"], case["expected"]):
            passed += 1
        print("-")

    print(f"Total: {passed}/{len(cases)}")
