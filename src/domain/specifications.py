from abc import ABC, abstractmethod

class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        pass
    def __and__(self, other):
        return AndSpecification(self, other)

class AndSpecification(Specification):
    def __init__(self, spec1, spec2):
        self.spec1 = spec1
        self.spec2 = spec2
    def is_satisfied_by(self, candidate) -> bool:
        return self.spec1.is_satisfied_by(candidate) and self.spec2.is_satisfied_by(candidate)

class ClienteActivoSpec(Specification):
    def is_satisfied_by(self, cliente) -> bool:
        return cliente.get("activo") == 1

class EsVipSpec(Specification):
    def is_satisfied_by(self, cliente) -> bool:
        return cliente.get("es_preferente") == 1

class DetalleNoVacioSpec(Specification):
    def is_satisfied_by(self, lineas_pedido) -> bool:
        return len(lineas_pedido) > 0