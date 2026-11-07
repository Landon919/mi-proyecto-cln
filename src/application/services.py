from src.domain.errores import ReglaDeNegocioError
from src.domain.modelos import Linea
from src.domain.pedido import Pedido
from src.domain.specifications import ProductoDisponibleSpec

# acción (API / CSV) -> método del agregado
ACCIONES = {
    "aprobar": "aprobar",
    "preparar": "iniciar_preparacion",
    "listo": "marcar_listo",
    "completar": "completar",
}


class PedidoService:
    """Orquesta casos de uso. No contiene reglas: viven en el dominio."""

    def __init__(self, pedidos, clientes, catalogo):
        self.pedidos = pedidos
        self.clientes = clientes
        self.catalogo = catalogo

    def crear_pedido(self, cliente_id, items, promocion_activa=False, autorizado=True):
        cliente = self.clientes.obtener_por_id(cliente_id)
        lineas = []
        for item in items:
            producto = self.catalogo.obtener_por_id(item["recurso_id"])
            if not ProductoDisponibleSpec(item["cantidad"]).is_satisfied_by(producto):
                raise ReglaDeNegocioError(
                    f"Producto no disponible o sin stock: {producto.id}")
            lineas.append(Linea(producto.id, item["cantidad"], producto.precio))
        pedido = Pedido.crear(cliente, lineas, promocion_activa, autorizado)
        self.pedidos.guardar(pedido)
        return pedido

    def ejecutar_accion(self, pedido_id, accion, motivo=None,
                        autorizado_por_encargado=False):
        pedido = self.pedidos.obtener_por_id(pedido_id)
        if accion == "cancelar":
            pedido.cancelar(motivo, autorizado_por_encargado)
        elif accion in ACCIONES:
            getattr(pedido, ACCIONES[accion])()
        else:
            raise ReglaDeNegocioError(f"Acción desconocida: {accion}")
        self.pedidos.guardar(pedido)
        return pedido

    def obtener_pedido(self, pedido_id):
        return self.pedidos.obtener_por_id(pedido_id)

    def evaluar_beneficio(self, pedido_id) -> bool:
        pedido = self.pedidos.obtener_por_id(pedido_id)
        cliente = self.clientes.obtener_por_id(pedido.cliente_id)
        return pedido.aplica_beneficio(cliente)