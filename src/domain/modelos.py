from dataclasses import dataclass
from decimal import Decimal

from src.domain.errores import ReglaDeNegocioError


@dataclass(frozen=True)
class Cliente:
    id: str
    nombre: str
    activo: bool
    es_preferente: bool


@dataclass(frozen=True)
class Producto:
    id: str
    descripcion: str
    precio: Decimal
    stock: int
    habilitado: bool


@dataclass(frozen=True)
class Linea:
    """Value Object: una línea del pedido. Inmutable y se valida al crearse."""
    recurso_id: str
    cantidad: int
    precio_unitario: Decimal

    def __post_init__(self):
        if self.cantidad <= 0:
            raise ReglaDeNegocioError("La cantidad debe ser mayor a cero")

    @property
    def subtotal(self) -> Decimal:
        return self.precio_unitario * self.cantidad