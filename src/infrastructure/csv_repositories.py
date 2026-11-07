import csv
from decimal import Decimal
from pathlib import Path

from src.domain.errores import EntidadNoEncontradaError
from src.domain.modelos import Cliente, Producto
from src.domain.repositorios import CatalogoRepository, ClienteRepository

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def _leer(nombre):
    with open(DATA_DIR / nombre, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


class CsvClienteRepository(ClienteRepository):
    def __init__(self):
        self._datos = {
            r["actor_id"]: Cliente(r["actor_id"], r["nombre"],
                                   r["activo"] == "1", r["es_preferente"] == "1")
            for r in _leer("actores.csv")
        }

    def obtener_por_id(self, cliente_id):
        try:
            return self._datos[cliente_id]
        except KeyError:
            raise EntidadNoEncontradaError(f"Cliente no encontrado: {cliente_id}")


class CsvCatalogoRepository(CatalogoRepository):
    def __init__(self):
        self._datos = {
            r["recurso_id"]: Producto(r["recurso_id"], r["descripcion"],
                                      Decimal(r["precio_mxn"]),
                                      int(r["capacidad_o_stock"]), r["habilitado"] == "1")
            for r in _leer("catalogo.csv")
        }

    def obtener_por_id(self, recurso_id):
        try:
            return self._datos[recurso_id]
        except KeyError:
            raise EntidadNoEncontradaError(f"Producto no encontrado: {recurso_id}")