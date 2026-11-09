# Sazón Urbano - Sistema de gestión de pedidos

Producto Integrador de Aprendizaje - Componentes de Lógica de Negocio (UANL FIME).

- **Repositorio:** <[URL del repo en GitHub](https://github.com/Landon919/mi-proyecto-cln.git)>
- **Sistema desplegado:** <[URL de Rende](https://sazon-urbano.onrender.com/)r>
- **Swagger UI:** <[URL de Render](https://sazon-urbano.onrender.com/docs)>

## Equipo
- Landon Alexander Bautista Hernandez (2101662)

## Descripción
Sazón Urbano es un restaurante con atención en mesa, pedidos para llevar y entrega a
domicilio. Este sistema implementa el ciclo de vida del pedido aplicando las reglas del
negocio definidas en el BRD, con DDD, Specification, State Machine y una API REST documentada.

## Arquitectura
Capas con dependencias hacia el dominio:

| Capa | Carpeta | Contenido |
|---|---|---|
| Dominio | `src/domain` | Aggregate `Pedido` con State Machine, Value Object `Linea`, Specifications, interfaces de repositorio |
| Aplicación | `src/application` | `PedidoService`: orquesta casos de uso, sin reglas de negocio |
| Infraestructura | `src/infrastructure` | Repositorio SQLAlchemy (pedidos) y repositorios CSV (clientes y catálogo) |
| API | `src/api` | Endpoints FastAPI y traducción de errores a HTTP |

Patrones: Domain Model, Specification, State Machine, Repository, inyección de dependencias.
Decisiones: ver `docs/architecture/` (ADR) y `docs/trazabilidad.md`.

## Estructura del repositorio
```
docs/            BRD, user stories, glosario, BPMN, trazabilidad
  architecture/  ADRs y diagramas UML
  api/           especificación OpenAPI
src/             código (domain, application, infrastructure, api)
data/            datasets CSV (clientes, catálogo, casos de prueba)
tests/           pruebas unitarias e integración
.github/workflows/  CI/CD
```

## Ejecución con Docker (recomendada)
```bash
cp .env.example .env
docker compose up --build
```
API en http://localhost:8000 y Swagger en http://localhost:8000/docs

## Ejecución local (SQLite)
```bash
pip install -r requirements.txt
uvicorn src.api.main:app --reload
```

## Pruebas
```bash
python -m pytest --cov=src --cov-report=term-missing          # local
docker compose --profile test run --rm tests                  # con PostgreSQL
```
La cobertura mínima exigida es 80% (el CI falla si baja).

## Variables de entorno
Ver `.env.example`. `DATABASE_URL` define la base de datos; si no existe se usa SQLite local.

## Endpoints principales
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/pedidos` | Crear pedido (valida cliente, detalle, autorización y stock) |
| GET | `/pedidos/{id}` | Consultar pedido |
| POST | `/pedidos/{id}/acciones` | `aprobar`, `preparar`, `listo`, `completar`, `cancelar` |
| GET | `/pedidos/{id}/beneficio` | Evalúa el beneficio para cliente VIP |

Códigos: 201 creado, 404 no encontrado, 409 regla de negocio violada, 422 datos inválidos.

## Guion de demostración
1. Crear pedido con cliente activo `PED-C001` y producto `PED-P001` (201).
2. Crear pedido con cliente inactivo `PED-C007` (409, Specification).
3. Pasar por `aprobar`, `preparar`, `listo`, `completar`.
4. Intentar `completar` sobre un pedido nuevo (409, State Machine).
5. Cancelar en preparación sin y con `autorizado_por_encargado`.
6. Consultar `/beneficio` del cliente VIP `PED-C005` con y sin promoción activa.

## Documentación
- [BRD](docs/BRD.md) · [Trazabilidad](docs/trazabilidad.md) · [ADRs](docs/architecture/) · [OpenAPI](docs/api/openapi.json)

## Alcance
Se implementa el aggregate Pedido de punta a punta. El resto del diseño (Inventario, Pago,
Entrega, Lealtad) está documentado en el reporte; ver `docs/architecture/ADR-04-alcance-implementacion.md`.
