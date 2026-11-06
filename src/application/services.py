from src.domain.state_machine import EstadoPedido, PedidoStateMachine
from src.domain.specifications import ClienteActivoSpec, DetalleNoVacioSpec
from src.infrastructure.repositories import db_en_memoria

class PedidoService:
    def crear_pedido(self, actor_id: str, lineas: list):
        cliente = db_en_memoria.actores.get(actor_id)
        if not cliente:
            raise ValueError("Cliente no encontrado")
            
        # Aplicamos el Specification Pattern que exige tu PIA
        regla_cliente = ClienteActivoSpec()
        regla_detalle = DetalleNoVacioSpec()
        
        if not regla_cliente.is_satisfied_by(cliente):
            raise ValueError("El cliente no está activo")
        if not regla_detalle.is_satisfied_by(lineas):
            raise ValueError("El pedido no tiene detalle")

        # Generamos un ID simple para el pedido
        pedido_id = f"PED-{len(db_en_memoria.pedidos) + 1}"
        db_en_memoria.pedidos[pedido_id] = {
            "pedido_id": pedido_id,
            "actor_id": actor_id,
            "estado": EstadoPedido.CREADO.value,
            "lineas": lineas
        }
        return db_en_memoria.pedidos[pedido_id]

    def avanzar_estado(self, pedido_id: str, nuevo_estado: str):
        pedido = db_en_memoria.pedidos.get(pedido_id)
        if not pedido:
            raise ValueError("Pedido no encontrado")
            
        estado_actual = EstadoPedido(pedido["estado"])
        estado_destino = EstadoPedido(nuevo_estado)
        
        # Aplicamos la State Machine que exige tu PIA
        if not PedidoStateMachine.puede_transicionar(estado_actual, estado_destino):
            raise ValueError(f"Transición inválida de {estado_actual.value} a {estado_destino.value}")
            
        pedido["estado"] = estado_destino.value
        return pedido