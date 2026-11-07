import pytest

from src.domain.errores import EntidadNoEncontradaError, ReglaDeNegocioError

ITEM = [{"recurso_id": "PED-P001", "cantidad": 2}]


def test_crear_pedido(servicio):
    p = servicio.crear_pedido("PED-C001", ITEM)
    assert p.estado.value == "CREADO"


def test_cliente_inexistente(servicio):
    with pytest.raises(EntidadNoEncontradaError):
        servicio.crear_pedido("NO-EXISTE", ITEM)


def test_producto_inexistente(servicio):
    with pytest.raises(EntidadNoEncontradaError):
        servicio.crear_pedido("PED-C001", [{"recurso_id": "NO", "cantidad": 1}])


def test_producto_deshabilitado(servicio):
    with pytest.raises(ReglaDeNegocioError):
        servicio.crear_pedido("PED-C001", [{"recurso_id": "PED-P011", "cantidad": 1}])


def test_sin_stock(servicio):
    with pytest.raises(ReglaDeNegocioError):
        servicio.crear_pedido("PED-C001", [{"recurso_id": "PED-P001", "cantidad": 9999}])


def test_accion_desconocida(servicio):
    p = servicio.crear_pedido("PED-C001", ITEM)
    with pytest.raises(ReglaDeNegocioError):
        servicio.ejecutar_accion(p.id, "volar")


def test_cancelar_con_motivo(servicio):
    p = servicio.crear_pedido("PED-C001", ITEM)
    p = servicio.ejecutar_accion(p.id, "cancelar", motivo="Prueba")
    assert p.estado.value == "CANCELADO"
    assert servicio.obtener_pedido(p.id).motivo_cancelacion == "Prueba"