from enum import Enum

class EstadoPedido(str, Enum):
    CREADO = "CREADO"
    CONFIRMADO = "CONFIRMADO"
    EN_PREPARACION = "EN_PREPARACION"
    LISTO = "LISTO"
    ENTREGADO = "ENTREGADO"
    CANCELADO = "CANCELADO"

class PedidoStateMachine:
    transiciones_validas = {
        EstadoPedido.CREADO: [EstadoPedido.CONFIRMADO, EstadoPedido.CANCELADO],
        EstadoPedido.CONFIRMADO: [EstadoPedido.EN_PREPARACION, EstadoPedido.CANCELADO],
        EstadoPedido.EN_PREPARACION: [EstadoPedido.LISTO, EstadoPedido.CANCELADO],
        EstadoPedido.LISTO: [EstadoPedido.ENTREGADO],
        EstadoPedido.ENTREGADO: [],
        EstadoPedido.CANCELADO: []
    }

    @staticmethod
    def puede_transicionar(estado_actual: EstadoPedido, nuevo_estado: EstadoPedido) -> bool:
        return nuevo_estado in PedidoStateMachine.transiciones_validas.get(estado_actual, [])