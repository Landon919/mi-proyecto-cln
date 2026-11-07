## 01 ENTREVISTA SIMULADA

## Guía de preguntas (28 preguntas)

## Categoría 1: Proceso de pedidos (P1-P5)

- 1. ¿Qué eventos inician formalmente un pedido en cada canal (mesa, teléfono, WhatsApp, domicilio)?

- 2. ¿Quién tiene autorización para modificar un pedido después de registrado?

- 3. ¿En qué momento un pedido se considera “confirmado” y no puede cancelarse sin penalización?

- 4. ¿Cómo se manejan las modificaciones complejas (ej. cambiar proteína, combinar menús)?

- 5. ¿Cuál es el tiempo máximo aceptable desde que se toma el pedido hasta que se entrega?

## Categoría 2: Inventario y abastecimiento (P6-P10)

- 6. ¿Con qué frecuencia se actualiza el inventario actualmente y quien lo hace?

- 7. ¿Qué productos son críticos y como se maneja su falta?

- 8. ¿Cómo se registran las mermas y perdidas de ingredientes?

- 9. ¿Existen proveedores alternativos para ingredientes clave?

- 10. ¿Cómo se determina el punto de reorden (stock mínimo)?

## Categoría 3: Roles y permisos (P11-P15)

- 11. ¿Qué puede hacer un mesero que no pueda hacer un repartidor?

- 12. ¿Quién autoriza promociones y descuentos especiales?

- 13. ¿Quién puede cancelar un pedido ya en cocina?

14. ¿Cómo se asignan los pedidos a los repartidores?

- 15. ¿Qué reportes puede ver cada rol (mesero, encargado, gerente)?

## Categoría 4: Excepciones y contingencias (P16-P20)

- 16. ¿Qué sucede si un producto se agota después de tomar el pedido?

- 17. ¿Cómo se maneja un pedido incorrecto entregado al cliente?

- 18. ¿Qué protocolo hay para un pedido que no fue recogido por el repartidor?

- 19. ¿Cómo se gestionan las promociones cuando coinciden con falta de stock?

- 20. ¿Qué pasa con los pedidos en proceso si hay un corte de energía o falla del sistema?

## Categoría 5: Pagos y facturación (P21-P24)

- 21. ¿Qué métodos de pago se aceptan actualmente y como se registran?


- 22. ¿Cómo se manejan las propinas y su distribución?

- 23. ¿Se emiten facturas o comprobantes fiscales?¿Cómo se gestionan?

- 24. ¿Cómo se concilian los pagos al final del día?

## Categoría 6: Clientes y retroalimentación (P25-P28)

- 25. ¿Cómo se registra la información de clientes frecuentes?

- 26. ¿Existe algún programa de lealtad o puntos?

- 27. ¿Cómo se recopilan quejas o sugerencias de clientes?

- 28. ¿Se realiza seguimiento post-venta (encuesta, llamadas)?

## Transcripción de puntos clave [Archivo Excel]

Stakeholder: Gerente operativo – Sr. Roberto Martínez [Nombre de cliente inventado]

Fecha: 2 de septiembre de 2026

Duración: Aproximadamente 50 minutos

## Análisis de impacto de la entrevista

| Hallazgo | Impacto de requerimientos |
| --- | --- |
| Cada canal usa formato distinto | Diseñar interfaz unificada adaptable por canal |
|   | Modificaciones se pierden en papel Campos estructurados con validación |
| No hay confirmación formal de pedido | Implementar workflow con estados y reglas de transición |
| Inventario solo al final del día | Módulo de inventario en tiempo real con descuento automático |
| Mermas no se registran | Módulo obligatorio de mermas con foto y justificación |
| No hay punto de reorden definido | Sistema con cálculo automático basado en histórico |
| Roles difusos | Modelo de permisos claro por rol y acción |
| Promociones sin control de stock | Validación de stock y límites por promoción |
| No hay plan de contingencia | Módulo offline y sincronización automática |
| Múltiples métodos de pago sin registro | Módulo de pagos con soporte multi-método y estados por transacción |
| Propinas no registradas ni distribuidas equitativamente | Registro de propinas por pedido y reporte para reparto |
| Facturación manual y propensa a olvidos | Generación de tickets digitales y gestión de solicitudes de factura |
| Conciliación de caja manual con diferencias | Reporte automático de cierre de caja por método de pago |
| Falta de base de datos de clientes | Módulo de gestión de clientes con historial y preferencias |
| Sin programa de lealtad formal | Motor de puntos/recompensas configurable |


## 02 BRD – BUSINESS REQUIREMENTS DOCUMENT

## 1. Contexto del negocio

Sazón Urbano es un restaurante que ofrece servicio en mesa, para llevar y entrega a domicilio. Su operación depende de la coordinación entre cocina, caja, meseros y repartidores. Los ingresos provienen de alimentos, bebidas, paquetes y complementos.

Actualmente, el registro de pedidos, control de inventario, pagos y comunicación entre áreas se realiza de forma manual y con herramientas básicas (teléfono, WhatsApp, papel), lo que genera errores, demoras, pérdidas y falta de trazabilidad.

## Volumen operativo:

- 80-120 pedidos diarios en días regulares

- Picos de hasta 150 pedidos en fines de semana

- Inventario con 150+ ingredientes activos

- 8-12 empleados en turno completo

- Métodos de pago: efectivo, tarjeta, transferencia

## 2. Problema fundamental y oportunidad

## Problema:

- Productos agotados no se reflejan en tiempo real

- Cocina recibe pedidos incompletos o con modificaciones mal registradas

- Diferencias entre ventas e inventario físico (8% de desperdicio)

- Dificultad para rastrear cancelaciones y modificaciones

- Tiempo promedio de entrega: 45 minutos (estándar industrial: 30 minutos)

- 15% de pedidos presentan errores

- Pagos no conciliados y propinas sin control

- Falta de información de clientes y retroalimentación

## Oportunidad:

Implementar un sistema digital que integre pedidos, inventario, pagos, clientes y comunicación entre roles, reduciendo errores, mejorando la experiencia del cliente y optimizando la operación.

## Beneficios esperados:

- Reducción del tiempo de ciclo del pedido en un 25%


- Disminución de errores de preparación en un 90%

- Mejora de la rotación de inventario en un 30%

- Aumento de capacidad de atención sin incrementar personal

- Reducción de diferencias de caja en un 80%

- Incremento de clientes recurrentes en un 15%

## 3. Stakeholders y roles

| Rol | Responsabilidad | Expectativa |
| --- | --- | --- |
| Cliente | Solicitar y recibir pedido | Pedido correcto, a tiempo y con pago sencillo |
| Mesero/Caja | Tomar pedido, cobrar, coordinar | Herramienta rápida e intuitiva para pedidos y pagos |
| Cocina | Preparar pedidos | Información clara y completa |
| Encargado | Supervisar operación e inventario | Control total incluyendo caja y quejas |
| Repartidor | Entregar a domicilio | Ruta óptica y pedidos claros |
| Gerente | Tomar decisiones estratégicas | Datos confiables, incluyendo ventas, clientes y satisfacción |

## 4. Alcance

## Dentro del alcance:

- Gestión integral de pedidos (mesa, para llevar, domicilio)

- Control de inventario en tiempo real

- Asignación y seguimiento de repartidores

- Gestión de promociones y descuentos

- Gestión de pagos (efectivo, tarjeta, transferencia) y propinas

- Emisión de tickets y gestión de facturas

- Base de datos de clientes con historial y preferencias

- Registro de quejas y sugerencias

- Programa de lealtad básico

- Reportes operativos (ventas, inventario, errores, caja)

- Historial de clientes y pedidos

## Fuera del alcance:

- Sistema de contabilidad o nómina completo (solo reportes básicos)

- App móvil para clientes (fase 2)

- Integración con plataformas externas (Rappi, Uber Eats) – Fase 3

- Pasarela de pagos en línea (solo registro, no procesamiento)


## 5. Requerimientos funcionales

| ID | Requerimiento | Prioridad |
| --- | --- | --- |
| RF-01 | Registrar pedidos con productos, cantidades y modificaciones Must Have |   |
| RF-02 | Consultar disponibilidad de productos en tiempo real | Must Have |
| RF-03 | Enviar pedidos automáticamente a la estación de cocina correspondiente | Must Have |
| RF-04 | Actualizar inventario tras cada preparación y entrega | Must Have |
| RF-05 | Gestionar cancelaciones y devoluciones con diferentes niveles de autorización | Should Have |
| RF-06 | Administrar promociones con condiciones de tiempo y monto | Could Have |
| RF-07 | Asignar pedidos a domicilio a repartidores disponibles | Should Have |
| RF-08 | Generar reportes de ventas, inventario y errores | Should Have |
| RF-09 | Registrar mermas con categorías y justificación | Should Have |
| RF-10 | Consultar historial de pedidos por cliente | Could Have |
| RF-11 | Enviar notificaciones push por evento relevante | Should Have |
| RF-12 | Registrar pagos con método (efectivo, tarjeta, transferencia) y monto exacto | Must Have |
| RF-13 | Registrar propinas por pedido y asignarlas al mesero responsable | Should Have |
| RF-14 | Generar ticket digital por pedido y registrar solicitudes de factura | Should Have |
| RF-15 | Generar reporte de cierre de caja con conciliación por método de pago | Must Have |
| RF-16 | Gestionar base de datos de clientes con datos de contacto e historial | Should Have |
| RF-17 | Registrar quejas y sugerencias con categoría, resolución y seguimiento | Should Have |
| RF-18 | Administrar programa de lealtad con puntos acumulables y recompensas | Could Have |
|   | RF-19 Enviar encuesta de satisfacción post-entrega (opcional) | Could Have |

## 6. Requerimientos no funcionales

| ID | Requerimiento | Descripción |
| --- | --- | --- |
| RNF-01 | Rendimiento | Tiempo de respuesta < 2 segundos en operaciones críticas |
| RNF-02 |   | Disponibilidad Sistema disponible 12 horas diarias (8:00 am – 10:00 pm) |
| RNF-03 | Usabilidad | Interfaz adaptable a tablets y dispositivos móviles |
| RNF-04 |   | Escalabilidad Capacidad para 200 pedidos concurrentes |
| RNF-05 | Seguridad | Roles y permisos diferenciados por usuario |
| RNF-06 | Respaldo | Backup automático cada hora |
| RNF-07 |   | Modo offline Operación sin conexión con sincronización posterior |
| RNF-08 | Seguridad de pagos | Cumplir con estándares PCI DSS para el manejo de datos de tarjetas (aunque no se almacenen) |


## 7. Restricciones

- Presupuesto limitado (software open Source preferente)

- Personal con baja alfabetización digital

- Infraestructura de WiFi básica en el local

- Tiempo de implementación: 8 semanas

## 8. Supuestos

- El personal recibirá capacitación de 2 días

- La conectividad a internet será estable durante el horario laboral

- Los precios y promociones serán definidos por el gerente

- Los datos históricos serán migrados manualmente

- Los pagos con tarjeta seguirán procesándose con terminal bancaria externa; el sistema solo registrará la transacción

## 9. Criterios de éxito medibles

- 100% de pedidos registrados digitalmente (eliminar papel)

- < 2% de pedidos con errores de preparación

- Inventario con precisión > 98%

- Tiempo promedio de entrega <= 30 minutos

- Satisfacción del cliente >= 4.5/5 en encuestas

- Reducción del 20% en mermas de ingredientes

- Diferencias de caja < 1% del total de ventas

- Incremento del 15% en clientes recurrentes

## 10. Riesgos identificados

| Riesgo | Probabilidad Impacto |   | Mitigación |
| --- | --- | --- | --- |
| Resistencia al cambio | Alta | Medio | Capacitación y acompañamiento |
| Fallas técnicas | Media | Alto | Plan de contingencia y soporte |
| Datos incorrectos en migración | Media | Medio | Validación y pruebas exhaustivas |
| Integración con apps externas | Baja | Medio | Módulos separados en fases |
| Problemas de seguridad en pagos | Media | Alto | No almacenar datos de tarjeta, usar terminal externa, cifrado en tránsito |
| Baja adopción del programa de lealtad | Media | Bajo | Campañas de comunicación y recompensas atractivas |


## 11. Priorización MoSCoW

| Prioridad | Requerimientos |
| --- | --- |
| Must Have | Registro de pedidos, inventario en tiempo real, visualización en cocina, registro de pagos, cierre de caja |
| Should Have | Cancelaciones, asignación de repartidores, reportes básicos, propinas, tickets/facturas, gestión de clientes, quejas |
| Could Have | Promociones automáticas, reportes avanzados, programa de lealtad, encuestas |
| Won’t Have (ahora) | App móvil para clientes, integración con externos, pasarela de pagos propia |
