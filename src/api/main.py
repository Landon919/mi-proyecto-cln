from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.application.services import PedidoService

# Esto genera automáticamente tu Swagger UI
app = FastAPI(
    title="Sazón Urbano API", 
    description="API con DDD, Specification y State Machine para el PIA"
)
pedido_service = PedidoService()

class LineaPedido(BaseModel):
    recurso_id: str
    cantidad: int

class CrearPedidoRequest(BaseModel):
    actor_id: str
    lineas: List[LineaPedido]

@app.post("/pedidos/")
def registrar_pedido(req: CrearPedidoRequest):
    try:
        # Convertimos las lineas a formato diccionario para el servicio
        lineas_dict = [{"recurso_id": l.recurso_id, "cantidad": l.cantidad} for l in req.lineas]
        return pedido_service.crear_pedido(req.actor_id, lineas_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/pedidos/{pedido_id}/estado")
def cambiar_estado(pedido_id: str, nuevo_estado: str):
    try:
        return pedido_service.avanzar_estado(pedido_id, nuevo_estado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))