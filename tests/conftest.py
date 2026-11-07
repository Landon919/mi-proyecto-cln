import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_sazon.db")

import pytest  # noqa: E402

from src.application.services import PedidoService  # noqa: E402
from src.domain.errores import EntidadNoEncontradaError  # noqa: E402
from src.domain.repositorios import PedidoRepository  # noqa: E402
from src.infrastructure import models  # noqa: E402,F401
from src.infrastructure.csv_repositories import (  # noqa: E402
    CsvCatalogoRepository, CsvClienteRepository)
from src.infrastructure.database import Base, engine  # noqa: E402

Base.metadata.create_all(engine)


class MemoriaPedidoRepository(PedidoRepository):
    def __init__(self):
        self.datos = {}

    def guardar(self, pedido):
        self.datos[pedido.id] = pedido

    def obtener_por_id(self, pedido_id):
        if pedido_id not in self.datos:
            raise EntidadNoEncontradaError(pedido_id)
        return self.datos[pedido_id]


@pytest.fixture
def servicio():
    return PedidoService(MemoriaPedidoRepository(), CsvClienteRepository(),
                         CsvCatalogoRepository())