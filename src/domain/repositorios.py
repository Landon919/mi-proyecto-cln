from abc import ABC, abstractmethod


class PedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido): ...

    @abstractmethod
    def obtener_por_id(self, pedido_id): ...


class ClienteRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, cliente_id): ...


class CatalogoRepository(ABC):
    @abstractmethod
    def obtener_por_id(self, recurso_id): ...