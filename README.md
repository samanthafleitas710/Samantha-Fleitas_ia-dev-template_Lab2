# Proyecto Final · Samantha Fleitas

Agente RAG que responde preguntas sobre el PRD "Historial de Transacciones LegacyPay". Basado en el patrón ReAct con retriever lexical sobre `docs/prd/PRD.md`.

## Cómo probarlo en 5 minutos

### 1. Clonar y sincronizar

```bash
git clone <url-de-tu-fork>
cd ia-dev-template
git checkout proyecto-final
uv sync --extra llm
```

### 2. Levantar el Mock LLM en una terminal aparte

```bash
uv run --frozen uvicorn app.mock_llm:mock_app --port 8001
```

### 3. Correr el agente

```bash
uv run --frozen python -c "
from openai import OpenAI
from app.agent.loop import run_agent
client = OpenAI(base_url='http://localhost:8001/v1', api_key='mock')
print(run_agent('¿cuál es el rango máximo del historial?', client))"
```

### 4. Correr el Eval Set

```bash
uv run --frozen python evals/eval_agent.py
```

## Arquitectura del agente

- **Tools:** `buscar_regla_prd`, registrada en `app/agent/tools.py`.
- **Loop:** patrón ReAct con `MAX_STEPS = 5`.
- **RAG:** retriever lexical sobre `docs/prd/PRD.md`.
- **Log auditable:** cada paso se serializa en `logs/agent_run.jsonl`.

## Barandas aplicadas

- **Scope explícito:** definido en `SYSTEM_PROMPT`, dentro de `app/agent/loop.py`.
- **Budget:** límite de iteraciones mediante `MAX_STEPS = 5`, dentro de `app/agent/loop.py`.

## Criterios de aceptación

- [x] Al menos 2 de 3 casos del Eval Set pasan.
- [x] Cada corrida genera un log auditable en `logs/agent_run.jsonl`.
- [x] El agente se abstiene ante preguntas fuera de alcance.
- [ ] CI verde en GitHub Actions.

## Limitaciones conocidas

- El retriever es lexical y no utiliza embeddings, por lo que puede fallar ante sinónimos o formulaciones diferentes.
- El Mock LLM es determinístico y no cubre el 100 % de los comportamientos posibles de un LLM real.