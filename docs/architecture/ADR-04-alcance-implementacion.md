# ADR-04: Alcance de la implementación del PIA

**Estado:** Aceptado

## Contexto
En la Unidad 3 se diseñó una arquitectura con siete aggregates (Pedido, Promoción,
Inventario, Entrega, Repartidor, Pago y Cliente), nueve commands con handlers,
cuatro queries y una Unit of Work por solicitud (ADR-01, ADR-02 y ADR-03).
Para el PIA el equipo debe entregar una solución funcional, probada, contenerizada
y desplegada en el plazo de entrega.

## Alternativas
1. Implementar los siete aggregates completos: no es viable en el plazo y arriesga
   entregar un sistema que no ejecuta.
2. Implementar el aggregate central con todos los componentes obligatorios del curso
   (DDD, Specification, State Machine, API REST, persistencia, pruebas, CI/CD) y dejar
   el resto documentado.

## Decisión
Se implementa el aggregate **Pedido** de punta a punta (dominio, aplicación,
infraestructura y API). Cliente y Catálogo se consumen como datos de solo lectura
desde archivos CSV (carpeta `data/`). Los pedidos se guardan en una base de datos
relacional (PostgreSQL en Docker y producción; SQLite en pruebas locales).

Desviaciones respecto al diseño de U3:
- Un solo `PedidoService` orquesta los casos de uso en lugar de nueve handlers
  (CQRS básico queda como trabajo futuro, ADR-03).
- Cada `guardar` del repositorio es una transacción; no hay Unit of Work multi-aggregate
  porque cada caso de uso modifica un solo aggregate (ADR-02).
- Se mantiene la decisión de no implementar control de concurrencia.
- El stock del catálogo es estático (no se descuenta al preparar).
- El estado inicial del pedido se llama `CREADO` (equivale a `REGISTRADO` en el diseño de U3).

## Consecuencias
- Beneficios: el sistema corre, está probado y desplegado; el núcleo del dominio
  (State Machine y Specifications) es completo y demostrable.
- Costos: Inventario, Pago, Entrega y Lealtad no existen en código, por lo que RN-10 a RN-17
  quedan sin implementar. Siguen documentados en el reporte de U3.
- Trabajo posterior: agregar Inventario (merma) y Pago como nuevos aggregates reutilizando
  los patrones ya implementados.

## Trazabilidad
RF-01, RF-02, RF-05 · US-01, US-09 · RN-01, RN-03, RN-04 · CU-01, CU-03