from enum import Enum
from uuid import uuid4

from src.domain.errores import ReglaDeNegocioError
from src.domain.specifications import (
    ClienteActivoSpec, DetalleNoVacioSpec, AutorizadoSpec, ContextoPedido,
    APLICA_BENEFICIO,
)


class EstadoPedido(str, Enum):
    CREADO = "CREADO"
    CONFIRMADO = "CONFIRMADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"


E = EstadoPedido
# State Machine: tabla de transiciones permitidas
TRANSICIONES = {
    E.CREADO: {E.CONFIRMADO, E.CANCELADO},
    E.CONFIRMADO: {E.EN_PREPARACION, E.CANCELADO},
    E.EN_PREPARACION: {E.LISTO, E.CANCELADO},
    E.LISTO: {E.ENTREGADO},
    E.ENTREGADO: set(),
    E.CANCELADO: set(),
}

# Reglas que se evalúan al crear, con el mensaje de error de cada una
_REGLAS_CREACION = [
    (ClienteActivoSpec(), "El cliente no está activo"),
    (DetalleNoVacioSpec(), "El pedido no tiene detalle"),
    (AutorizadoSpec(), "El pedido no está autorizado"),
]


class Pedido:
    """Aggregate root. Protege sus invariantes y su ciclo de vida."""

    def __init__(self, id, cliente_id, lineas, estado=E.CREADO,
                 promocion_activa=False, autorizado=True, motivo_cancelacion=None):
        self.id = id
        self.cliente_id = cliente_id
        self.lineas = list(lineas)
        self.estado = EstadoPedido(estado)
        self.promocion_activa = promocion_activa
        self.autorizado = autorizado
        self.motivo_cancelacion = motivo_cancelacion
        self.eventos: list[str] = []   # eventos de dominio

    @classmethod
    def crear(cls, cliente, lineas, promocion_activa=False, autorizado=True):
        """Fábrica: aplica las Specifications de creación."""
        ctx = ContextoPedido(cliente, lineas, autorizado, promocion_activa)
        for regla, mensaje in _REGLAS_CREACION:
            if not regla.is_satisfied_by(ctx):
                raise ReglaDeNegocioError(mensaje)
        pedido = cls(f"PED-{uuid4().hex[:8].upper()}", cliente.id, lineas,
                     promocion_activa=promocion_activa, autorizado=autorizado)
        pedido.eventos.append("PedidoCreado")
        return pedido

    @property
    def total(self):
        return sum((l.subtotal for l in self.lineas), start=0)

    def aplica_beneficio(self, cliente) -> bool:
        ctx = ContextoPedido(cliente, self.lineas, self.autorizado, self.promocion_activa)
        return APLICA_BENEFICIO.is_satisfied_by(ctx)

    # --- State Machine ---
    def _transitar(self, nuevo: EstadoPedido, evento: str):
        if nuevo not in TRANSICIONES[self.estado]:
            raise ReglaDeNegocioError(
                f"Transición inválida: {self.estado.value} -> {nuevo.value}")
        self.estado = nuevo
        self.eventos.append(evento)

    def aprobar(self):
        self._transitar(E.CONFIRMADO, "PedidoConfirmado")

    def iniciar_preparacion(self):
        self._transitar(E.EN_PREPARACION, "PedidoEnPreparacion")

    def marcar_listo(self):
        self._transitar(E.LISTO, "PedidoListo")

    def completar(self):
        self._transitar(E.ENTREGADO, "PedidoEntregado")

    def cancelar(self, motivo: str, autorizado_por_encargado: bool = False):
        if self.estado == E.EN_PREPARACION and not autorizado_por_encargado:
            raise ReglaDeNegocioError(
                "Cancelar en preparación requiere autorización del encargado")
        if not motivo:
            raise ReglaDeNegocioError("Se requiere el motivo de cancelación")
        self._transitar(E.CANCELADO, "PedidoCancelado")
        self.motivo_cancelacion = motivo