from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidato) -> bool: ...

    def __and__(self, otra):
        return AndSpecification(self, otra)

    def __or__(self, otra):
        return OrSpecification(self, otra)

    def __invert__(self):
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, a: Specification, b: Specification):
        self.a, self.b = a, b

    def is_satisfied_by(self, c) -> bool:
        return self.a.is_satisfied_by(c) and self.b.is_satisfied_by(c)


class OrSpecification(Specification):
    def __init__(self, a: Specification, b: Specification):
        self.a, self.b = a, b

    def is_satisfied_by(self, c) -> bool:
        return self.a.is_satisfied_by(c) or self.b.is_satisfied_by(c)


class NotSpecification(Specification):
    def __init__(self, a: Specification):
        self.a = a

    def is_satisfied_by(self, c) -> bool:
        return not self.a.is_satisfied_by(c)


@dataclass
class ContextoPedido:
    """Los datos que las reglas necesitan para evaluar un pedido."""
    cliente: object          # Cliente
    lineas: list             # list[Linea]
    autorizado: bool = True
    promocion_activa: bool = False

    @property
    def total(self) -> Decimal:
        return sum((l.subtotal for l in self.lineas), Decimal("0"))


class ClienteActivoSpec(Specification):
    def is_satisfied_by(self, ctx) -> bool:
        return ctx.cliente.activo


class DetalleNoVacioSpec(Specification):
    def is_satisfied_by(self, ctx) -> bool:
        return len(ctx.lineas) > 0


class AutorizadoSpec(Specification):
    def is_satisfied_by(self, ctx) -> bool:
        return ctx.autorizado


class EsVipSpec(Specification):
    def is_satisfied_by(self, ctx) -> bool:
        return ctx.cliente.es_preferente


class TotalMinimoSpec(Specification):
    def __init__(self, minimo):
        self.minimo = Decimal(str(minimo))

    def is_satisfied_by(self, ctx) -> bool:
        return ctx.total >= self.minimo


class PromocionActivaSpec(Specification):
    def is_satisfied_by(self, ctx) -> bool:
        return ctx.promocion_activa


class ProductoDisponibleSpec(Specification):
    """Producto habilitado y con stock suficiente para la cantidad pedida (RN-01)."""
    def __init__(self, cantidad: int):
        self.cantidad = cantidad

    def is_satisfied_by(self, producto) -> bool:
        return producto.habilitado and producto.stock >= self.cantidad


PUEDE_CREARSE = ClienteActivoSpec() & DetalleNoVacioSpec() & AutorizadoSpec()
APLICA_BENEFICIO = EsVipSpec() & TotalMinimoSpec(1500) & ~PromocionActivaSpec()