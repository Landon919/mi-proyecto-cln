import csv
from collections import defaultdict
from decimal import Decimal

import pytest

from src.domain.errores import ReglaDeNegocioError
from src.infrastructure.csv_repositories import DATA_DIR


def _leer(nombre):
    with open(DATA_DIR / nombre, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


OPERACIONES = _leer("operaciones.csv")
TRANSICIONES = _leer("transiciones_prueba.csv")
CLIENTES = {c["actor_id"]: c for c in _leer("actores.csv")}
PRODUCTOS = {p["recurso_id"]: p for p in _leer("catalogo.csv")}
DETALLE = defaultdict(list)
for d in _leer("detalle_operaciones.csv"):
    DETALLE[d["operacion_id"]].append(
        {"recurso_id": d["recurso_id"], "cantidad": int(d["cantidad"])})


def _debe_fallar(op):
    """Regla del CSV: cliente activo AND detalle no vacío AND autorizado."""
    return (CLIENTES[op["actor_id"]]["activo"] == "0"
            or op["autorizado"] == "0"
            or not DETALLE[op["operacion_id"]])


def _producto_ok(i):
    p = PRODUCTOS[i["recurso_id"]]
    return p["habilitado"] == "1" and int(p["capacidad_o_stock"]) >= i["cantidad"]


FALLAN = [o for o in OPERACIONES if _debe_fallar(o)]
CREABLES = [o for o in OPERACIONES
            if not _debe_fallar(o) and all(_producto_ok(i) for i in DETALLE[o["operacion_id"]])]


def _crear(servicio, op):
    return servicio.crear_pedido(op["actor_id"], DETALLE[op["operacion_id"]],
                                 op["promocion_activa"] == "1", op["autorizado"] == "1")


@pytest.mark.parametrize("op", FALLAN, ids=lambda o: o["operacion_id"])
def test_operacion_invalida_es_rechazada(servicio, op):
    with pytest.raises(ReglaDeNegocioError):
        _crear(servicio, op)


@pytest.mark.parametrize("op", CREABLES, ids=lambda o: o["operacion_id"])
def test_evaluar_beneficio(servicio, op):
    """Regla del CSV: VIP AND total >= 1500 AND NOT promoción."""
    pedido = _crear(servicio, op)
    total = sum(Decimal(PRODUCTOS[i["recurso_id"]]["precio_mxn"]) * i["cantidad"]
                for i in DETALLE[op["operacion_id"]])
    esperado = (CLIENTES[op["actor_id"]]["es_preferente"] == "1"
                and total >= 1500 and op["promocion_activa"] == "0")
    assert servicio.evaluar_beneficio(pedido.id) == esperado


@pytest.mark.parametrize("caso", TRANSICIONES, ids=lambda c: c["caso_id"])
def test_transiciones_sugeridas(servicio, caso):
    p = servicio.crear_pedido("PED-C001", [{"recurso_id": "PED-P001", "cantidad": 1}])
    accion = caso["accion_sugerida"]
    if accion == "aprobar":
        assert servicio.ejecutar_accion(p.id, "aprobar").estado.value == "CONFIRMADO"
    elif accion == "cancelar":
        r = servicio.ejecutar_accion(p.id, "cancelar", motivo="Prueba")
        assert r.estado.value == "CANCELADO"
    elif accion == "completar":
        for paso in ["aprobar", "preparar", "listo", "completar"]:
            r = servicio.ejecutar_accion(p.id, paso)
        assert r.estado.value == "ENTREGADO"
    elif accion == "repetir_aprobacion":
        servicio.ejecutar_accion(p.id, "aprobar")
        with pytest.raises(ReglaDeNegocioError):
            servicio.ejecutar_accion(p.id, "aprobar")
    elif accion == "saltar_estado":
        with pytest.raises(ReglaDeNegocioError):
            servicio.ejecutar_accion(p.id, "listo")