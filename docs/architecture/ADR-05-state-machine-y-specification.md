# ADR-05: State Machine y Specification en el aggregate Pedido

**Estado:** Aceptado

## Contexto
Las reglas del pedido dependen de su estado (por ejemplo, cancelar exige autorización
solo si ya está en preparación) y de combinaciones de condiciones (cliente activo,
detalle no vacío, pedido autorizado; cliente VIP, total mínimo y sin promoción).
Estas reglas cambian con el negocio y deben aplicarse igual desde cualquier entrada.

## Alternativas
- `if` anidados dentro del servicio: las reglas se dispersan y se duplican.
- Campo de estado libre (texto) sin validar transiciones: permite estados inválidos.
- State Machine (tabla de transiciones dentro del aggregate) y Specifications
  componibles (`&`, `|`, `~`) en el dominio.

## Decisión
- La State Machine vive en `src/domain/pedido.py` como tabla `TRANSICIONES`; toda
  transición pasa por `_transitar`, que rechaza las inválidas con `ReglaDeNegocioError`.
- Las reglas de negocio son Specifications en `src/domain/specifications.py`.
  Se componen en `PUEDE_CREARSE` y `APLICA_BENEFICIO`.

## Consecuencias
- Beneficios: una regla se cambia en un solo lugar; las reglas se leen casi igual que en
  el dataset de casos de prueba; el principio Abierto/Cerrado se cumple (una regla nueva es
  una clase nueva).
- Costos: más clases que con condicionales simples.
- Riesgo: Pedido concentra comportamiento (ya identificado en la revisión SOLID de U3).

## Trazabilidad
US-09, US-10 · RN-03, RN-04 · casos_prueba.csv y transiciones_prueba.csv ·
`tests/unit/test_dominio.py`, `tests/integration/test_datos_csv.py`