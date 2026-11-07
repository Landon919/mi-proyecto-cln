from contextlib import asynccontextmanager
from functools import lru_cache
from typing import List, Literal, Optional

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.application.services import PedidoService
from src.domain.errores import EntidadNoEncontradaError, ReglaDeNegocioError
from src.infrastructure import models  # noqa: F401  (registra las tablas)
from src.infrastructure.csv_repositories import CsvCatalogoRepository, CsvClienteRepository
from src.infrastructure.database import Base, engine
from src.infrastructure.repositories import SqlPedidoRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Sazón Urbano API",
    description="API con DDD, Specification y State Machine (PIA - Componentes de Lógica de Negocio)",
    lifespan=lifespan,
)


@app.exception_handler(ReglaDeNegocioError)
async def regla_handler(request, exc):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(EntidadNoEncontradaError)
async def no_encontrado_handler(request, exc):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@lru_cache
def _clientes():
    return CsvClienteRepository()


@lru_cache
def _catalogo():
    return CsvCatalogoRepository()


def get_service() -> PedidoService:
    return PedidoService(SqlPedidoRepository(), _clientes(), _catalogo())


class LineaIn(BaseModel):
    recurso_id: str
    cantidad: int


class CrearPedidoRequest(BaseModel):
    cliente_id: str
    lineas: List[LineaIn]
    promocion_activa: bool = False
    autorizado: bool = True


class AccionRequest(BaseModel):
    accion: Literal["aprobar", "preparar", "listo", "completar", "cancelar"]
    motivo: Optional[str] = None
    autorizado_por_encargado: bool = False


def _a_dict(p):
    return {
        "id": p.id,
        "cliente_id": p.cliente_id,
        "estado": p.estado.value,
        "total": float(p.total),
        "promocion_activa": p.promocion_activa,
        "motivo_cancelacion": p.motivo_cancelacion,
        "lineas": [{"recurso_id": l.recurso_id, "cantidad": l.cantidad,
                    "precio_unitario": float(l.precio_unitario)} for l in p.lineas],
    }


@app.post("/pedidos", status_code=201)
def crear_pedido(req: CrearPedidoRequest, svc: PedidoService = Depends(get_service)):
    items = [l.model_dump() for l in req.lineas]
    return _a_dict(svc.crear_pedido(req.cliente_id, items, req.promocion_activa, req.autorizado))


@app.get("/pedidos/{pedido_id}")
def obtener_pedido(pedido_id: str, svc: PedidoService = Depends(get_service)):
    return _a_dict(svc.obtener_pedido(pedido_id))


@app.post("/pedidos/{pedido_id}/acciones")
def ejecutar_accion(pedido_id: str, req: AccionRequest,
                    svc: PedidoService = Depends(get_service)):
    return _a_dict(svc.ejecutar_accion(pedido_id, req.accion, req.motivo,
                                       req.autorizado_por_encargado))


@app.get("/pedidos/{pedido_id}/beneficio")
def beneficio(pedido_id: str, svc: PedidoService = Depends(get_service)):
    return {"pedido_id": pedido_id, "aplica_beneficio": svc.evaluar_beneficio(pedido_id)}