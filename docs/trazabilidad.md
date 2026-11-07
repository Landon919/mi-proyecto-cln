# Trazabilidad: análisis → arquitectura → código → pruebas

| Requisito / Historia | Regla | Dominio | Servicio | Endpoint | Tests |
|---|---|---|---|---|---|
| US-01 / RF-01: registrar pedido | Pedido con detalle, total calculado | `Pedido.crear`, `Linea` | `PedidoService.crear_pedido` | `POST /pedidos` | `test_crear_pedido_valido`, `test_crear_y_consultar_pedido` |
| US-01 (producto agotado) / RF-02 | RN-01: no confirmar sin stock | `ProductoDisponibleSpec` | `crear_pedido` | `POST /pedidos` (409) | `test_sin_stock`, `test_producto_deshabilitado`, `test_producto_deshabilitado_409` |
| Dataset: cliente activo, detalle no vacío, autorizado | `PUEDE_CREARSE` | `ClienteActivoSpec`, `DetalleNoVacioSpec`, `AutorizadoSpec` | `crear_pedido` | `POST /pedidos` (409) | `test_cliente_inactivo_no_puede_crear`, `test_detalle_vacio_no_puede_crear`, `test_no_autorizado_no_puede_crear`, `test_operacion_invalida_es_rechazada` |
| Entrevista P3, US-03, US-04: ciclo de vida del pedido | State Machine | `TRANSICIONES`, `Pedido._transitar` | `ejecutar_accion` | `POST /pedidos/{id}/acciones` | `test_flujo_completo_hasta_entregado`, `test_saltar_estado_falla`, `test_repetir_aprobacion_falla`, `test_transicion_invalida_409`, `test_transiciones_sugeridas` |
| US-09 / RF-05: cancelar antes de preparación | RN-03: sin autorización | `Pedido.cancelar` | `ejecutar_accion` | `POST /pedidos/{id}/acciones` | `test_cancelar_antes_de_preparacion_no_requiere_autorizacion` |
| US-09 / RF-05: cancelar en preparación | RN-04: exige encargado y motivo | `Pedido.cancelar` | `ejecutar_accion` | `POST /pedidos/{id}/acciones` | `test_cancelar_en_preparacion_sin_autorizacion_falla`, `test_cancelar_en_preparacion_con_autorizacion`, `test_cancelar_exige_motivo`, `test_cancelar_en_preparacion_requiere_autorizacion` |
| Descuento a cliente frecuente (P12) / US-18 / RF-18 | VIP, total ≥ 1500 y sin promoción | `APLICA_BENEFICIO` | `evaluar_beneficio` | `GET /pedidos/{id}/beneficio` | `test_specification_beneficio_*`, `test_beneficio_vip`, `test_beneficio_no_aplica_con_promocion`, `test_evaluar_beneficio` |
| RNF: persistencia | Pedido persiste entre solicitudes | `PedidoRepository` (interfaz) | — | — | `test_flujo_completo_persistido` |
| Manejo de errores (404/409/422) | Errores de negocio vs. no encontrado | `ReglaDeNegocioError`, `EntidadNoEncontradaError` | — | todos | `test_pedido_inexistente_404`, `test_cliente_inexistente_404`, `test_accion_invalida_422` |

## Fuera del alcance de código (ver ADR-04)
Inventario y mermas (RN-10, RN-11), Pago (RN-15, RN-16), Entrega y Repartidor (RN-12 a RN-14),
Cliente y lealtad con puntos (RN-17). Están diseñados en el reporte de la Unidad 3.