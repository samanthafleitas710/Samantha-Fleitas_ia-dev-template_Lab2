# Postmortem · Proyecto Final Samantha Fleitas · 2026-08-31

## Qué funcionó

- La construcción incremental del proyecto a lo largo de los laboratorios me permitió llegar al Proyecto Final con una base funcional ya validada.
- La integración entre FastAPI, el PRD y el agente ReAct permitió demostrar un flujo completo desde la consulta hasta la recuperación de evidencia.
- El uso de IA aceleró la generación del código inicial del agente (`tools.py`, `loop.py` y `logger.py`), reduciendo el tiempo de implementación.

## Qué no funcionó

- La integración inicial con el Mock LLM presentó problemas de compatibilidad entre el formato esperado por el agente y las respuestas generadas por el mock.
- Algunas correcciones requirieron más tiempo del esperado debido a errores en la comunicación entre el ciclo ReAct y la recuperación de evidencia.
- Varias sugerencias generadas por IA parecían correctas, pero necesitaron validación, auditoría constante y ajustes manuales para cumplir exactamente con la guía del laboratorio.

## Qué haría distinto

- Preparar desde etapas más tempranas los casos de prueba adversariales y los escenarios de validación del agente.
- Documentar cada decisión técnica durante el desarrollo para simplificar la elaboración de AI_USAGE.md y la defensa final.

## 3 lecciones aprendidas

1. Sobre agentes:
   Un agente necesita límites claros de alcance y ejecución. Sin guardrails explícitos puede intentar responder consultas fuera del dominio esperado.

2. Sobre RAG:
   Para un dominio pequeño y controlado, una búsqueda lexical simple puede ser suficiente para entregar respuestas fundamentadas en evidencia.

3. Sobre trabajo con IA:
   La IA acelera significativamente el desarrollo, pero siempre requiere revisión humana, validación funcional y pruebas antes de aceptar los resultados generados, como una buena auditoría por cada corrida.