from decimal import Decimal

from src.domain.errores import EntidadNoEncontradaError
from src.domain.modelos import Linea
from src.domain.pedido import Pedido
from src.domain.repositorios import PedidoRepository
from src.infrastructure.database import SessionLocal
from src.infrastructure.models import PedidoModel


class SqlPedidoRepository(PedidoRepository):
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def guardar(self, pedido: Pedido):
        with self.session_factory() as session:
            session.merge(PedidoModel(
                id=pedido.id,
                cliente_id=pedido.cliente_id,
                estado=pedido.estado.value,
                promocion_activa=pedido.promocion_activa,
                autorizado=pedido.autorizado,
                motivo_cancelacion=pedido.motivo_cancelacion,
                lineas=[{"recurso_id": l.recurso_id, "cantidad": l.cantidad,
                         "precio_unitario": str(l.precio_unitario)} for l in pedido.lineas],
            ))
            session.commit()

    def obtener_por_id(self, pedido_id: str) -> Pedido:
        with self.session_factory() as session:
            m = session.get(PedidoModel, pedido_id)
            if m is None:
                raise EntidadNoEncontradaError(f"Pedido no encontrado: {pedido_id}")
            lineas = [Linea(l["recurso_id"], l["cantidad"], Decimal(l["precio_unitario"]))
                      for l in m.lineas]
            return Pedido(m.id, m.cliente_id, lineas, m.estado, m.promocion_activa,
                          m.autorizado, m.motivo_cancelacion)