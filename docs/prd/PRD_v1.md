Estoy corrigiendo el documento para dejarlo alineado con el formato solicitado y sin contenido ajeno al PRD.

Estoy actualizando el documento para dejarlo en el formato de PRD solicitado, con secciones claras y las preguntas abiertas señaladas.

Got last terminal command

Estoy sustituyendo el contenido del PRD con una versión más limpia y consistente, manteniendo la separación entre hechos y propuestas.

Got last terminal command

El documento ya fue actualizado; estoy verificando su contenido final para asegurar que quede listo en el archivo.

Read [](file:///c%3A/Users/PYFleitaSa/Downloads/Samantha-Fleitas_ia-dev-template_Lab2/docs/prd/PRD_v1.md)

Estoy aplicando el contenido en el archivo y verificando que quede guardado correctamente.

Got last terminal command

Se está escribiendo el contenido final en el archivo para que quede disponible en el editor.

Read [](file:///c%3A/Users/PYFleitaSa/Downloads/Samantha-Fleitas_ia-dev-template_Lab2/docs/prd/PRD_v1.md)

# PRD preliminar — Historial de transacciones de LegacyPay

## 1. Visión y problema

### Hechos proporcionados
- LegacyPay es una pasarela B2B.
- Un comercio autorizado consulta transacciones de los últimos 90 días.
- Los filtros mínimos son fecha, estado y monto.
- La consulta debe ser paginada.
- No debe exponer datos completos de tarjeta ni datos de autenticación.
- El uso debe limitarse a datos sintéticos del caso.

### Propuesta
- Proporcionar un historial de transacciones consultable y seguro para el comercio autorizado, con filtros básicos y paginación, sin exponer información sensible.

### Problema
- Existe la necesidad de revisar transacciones de forma ordenada y segura, evitando la exposición de datos sensibles y facilitando la búsqueda de información relevante dentro de un rango temporal limitado.

---

## 2. Alcance incluido y fuera de alcance

### Alcance incluido
- Consultar transacciones de un comercio autorizado.
- Limitar la consulta al rango de los últimos 90 días.
- Aplicar filtros por fecha, estado y monto.
- Mostrar resultados de forma paginada.
- Restringir la exposición de datos sensibles, incluyendo la exclusión de datos completos de tarjeta y datos de autenticación.
- Utilizar únicamente datos sintéticos del escenario.

### Fuera de alcance
- Definir nuevas capacidades de reporte o análisis más allá del historial de transacciones.
- Incluir datos completos de tarjeta o datos de autenticación.
- Proponer cambios de arquitectura o dependencias no justificados por el alcance del producto.
- Definir políticas internas, reglas regulatorias u otros criterios no explicitados en los hechos.

### Preguntas abiertas
- PREGUNTA ABIERTA: ¿qué información adicional, si la hubiera, debe mostrarse en cada resultado de transacción?
- PREGUNTA ABIERTA: ¿qué comportamiento debe tener la paginación cuando no hay resultados para los filtros aplicados?

---

## 3. Usuarios, entidades y reglas de negocio

### Usuarios
- Comercio autorizado: usuario principal del flujo de consulta.
- PREGUNTA ABIERTA: ¿existe otro rol que deba consultar o administrar este historial?

### Entidades
- Transacción: registro principal del historial.
- Comercio autorizado: actor asociado a las transacciones consultables.
- Estado de la transacción: criterio de filtro y contexto de visualización.
- Fecha de la transacción: criterio de filtro.
- Monto de la transacción: criterio de filtro.
- Paginación: mecanismo para navegar los resultados.

### Reglas de negocio
- Solo un comercio autorizado puede consultar las transacciones correspondientes.
- La consulta se limita a transacciones de los últimos 90 días.
- Los filtros mínimos obligatorios son fecha, estado y monto.
- La respuesta debe presentarse de forma paginada.
- No se deben exponer datos completos de tarjeta ni datos de autenticación.
- El conjunto de datos debe ser sintético y consistente con el escenario.

### Preguntas abiertas
- PREGUNTA ABIERTA: ¿qué campos de la transacción deben mostrarse en la vista de resultados?
- PREGUNTA ABIERTA: ¿qué criterios de ordenamiento deben aplicarse dentro de la consulta?

---

## 4. Historias de usuario con criterios de aceptación

### Historia de usuario 1
Como comercio autorizado, quiero consultar el historial de transacciones de los últimos 90 días para revisar movimientos relevantes.

#### Criterios de aceptación
- El usuario puede consultar transacciones dentro del rango de los últimos 90 días.
- El sistema devuelve resultados asociados al comercio autorizado.
- Si no existen resultados en el rango solicitado, el sistema lo informa de forma clara.

### Historia de usuario 2
Como comercio autorizado, quiero filtrar transacciones por fecha, estado y monto para encontrar información específica.

#### Criterios de aceptación
- El usuario puede aplicar filtros por fecha, estado y monto.
- El sistema devuelve únicamente los resultados que cumplen con los filtros aplicados.
- Si un filtro no tiene coincidencias, el sistema muestra un resultado vacío o un mensaje apropiado.

### Historia de usuario 3
Como comercio autorizado, quiero ver los resultados de forma paginada para navegar el historial sin sobrecargar la vista.

#### Criterios de aceptación
- Los resultados se presentan en páginas.
- El usuario puede navegar entre páginas de resultados.
- La paginación permite consultar el conjunto completo de resultados sin exponerlos en una sola vista.

### Historia de usuario 4
Como comercio autorizado, quiero que la consulta no exponga datos sensibles para operar con seguridad.

#### Criterios de aceptación
- No se muestran datos completos de tarjeta.
- No se muestran datos de autenticación.
- La información presentada cumple con la restricción de no exponer datos sensibles.

### Preguntas abiertas
- PREGUNTA ABIERTA: ¿cuál es el número de resultados por página por defecto?
- PREGUNTA ABIERTA: ¿qué comportamiento debe tener la interfaz si el usuario aplica filtros que no devuelven resultados?

---

## 5. Restricciones no funcionales

### Hechos proporcionados
- La solución debe soportar consulta paginada.
- La solución debe evitar la exposición de datos sensibles.
- La solución debe operar sobre datos sintéticos.

### Propuesta
- La implementación debe priorizar claridad en la consulta, seguridad en la exposición de datos y consistencia con los datos sintéticos del caso.

### Restricciones
- No se deben exponer datos completos de tarjeta ni datos de autenticación.
- La información mostrada debe corresponder únicamente a datos sintéticos del escenario.
- La experiencia debe permitir la navegación de resultados mediante paginación.

### Preguntas abiertas
- PREGUNTA ABIERTA: ¿qué nivel de rendimiento se requiere para la consulta?
- PREGUNTA ABIERTA: ¿qué disponibilidad o continuidad operativa se espera para este flujo?
- PREGUNTA ABIERTA: ¿qué requisitos de auditoría o trazabilidad, si los hubiera, deben cumplirse?

---

## 6. Preguntas abiertas

- PREGUNTA ABIERTA: ¿qué campos concretos de la transacción deben mostrarse en la interfaz?
- PREGUNTA ABIERTA: ¿qué formato debe usarse para las fechas en los filtros y resultados?
- PREGUNTA ABIERTA: ¿cuál es el tamaño de página esperado por defecto?
- PREGUNTA ABIERTA: ¿qué orden debe aplicarse a los resultados al listar transacciones?
- PREGUNTA ABIERTA: ¿existen otros roles o permisos distintos al comercio autorizado que deban considerarse?
- PREGUNTA ABIERTA: ¿qué criterios definen si una transacción se considera visible o no para un usuario específico?
 


