from decimal import Decimal

import pytest

from src.domain.errores import ReglaDeNegocioError
from src.domain.modelos import Cliente, Linea
from src.domain.pedido import EstadoPedido, Pedido
from src.domain.specifications import (
    APLICA_BENEFICIO, ContextoPedido, EsVipSpec, PromocionActivaSpec, TotalMinimoSpec)

ACTIVO = Cliente("C1", "Ana", True, False)
INACTIVO = Cliente("C2", "Beto", False, False)
VIP = Cliente("C3", "Vera", True, True)
LINEAS = [Linea("P1", 2, Decimal("100"))]


def nuevo():
    return Pedido.crear(ACTIVO, LINEAS)


def test_crear_pedido_valido():
    p = nuevo()
    assert p.estado == EstadoPedido.CREADO
    assert p.total == Decimal("200")
    assert "PedidoCreado" in p.eventos


def test_cliente_inactivo_no_puede_crear():
    with pytest.raises(ReglaDeNegocioError):
        Pedido.crear(INACTIVO, LINEAS)


def test_detalle_vacio_no_puede_crear():
    with pytest.raises(ReglaDeNegocioError):
        Pedido.crear(ACTIVO, [])


def test_no_autorizado_no_puede_crear():
    with pytest.raises(ReglaDeNegocioError):
        Pedido.crear(ACTIVO, LINEAS, autorizado=False)


def test_linea_con_cantidad_cero_falla():
    with pytest.raises(ReglaDeNegocioError):
        Linea("P1", 0, Decimal("10"))


def test_flujo_completo_hasta_entregado():
    p = nuevo()
    p.aprobar()
    p.iniciar_preparacion()
    p.marcar_listo()
    p.completar()
    assert p.estado == EstadoPedido.ENTREGADO
    assert p.eventos[-1] == "PedidoEntregado"


@pytest.mark.parametrize("metodo", ["iniciar_preparacion", "marcar_listo", "completar"])
def test_saltar_estado_falla(metodo):
    with pytest.raises(ReglaDeNegocioError):
        getattr(nuevo(), metodo)()


def test_repetir_aprobacion_falla():
    p = nuevo()
    p.aprobar()
    with pytest.raises(ReglaDeNegocioError):
        p.aprobar()


def test_cancelar_antes_de_preparacion_no_requiere_autorizacion():
    p = nuevo()
    p.aprobar()
    p.cancelar("Cliente se arrepintió")
    assert p.estado == EstadoPedido.CANCELADO


def test_cancelar_en_preparacion_sin_autorizacion_falla():
    p = nuevo()
    p.aprobar()
    p.iniciar_preparacion()
    with pytest.raises(ReglaDeNegocioError):
        p.cancelar("Se fue")


def test_cancelar_en_preparacion_con_autorizacion():
    p = nuevo()
    p.aprobar()
    p.iniciar_preparacion()
    p.cancelar("Se fue", autorizado_por_encargado=True)
    assert p.estado == EstadoPedido.CANCELADO
    assert p.motivo_cancelacion == "Se fue"


def test_cancelar_exige_motivo():
    with pytest.raises(ReglaDeNegocioError):
        nuevo().cancelar("")


def test_estados_finales_no_transitan():
    p = nuevo()
    p.cancelar("x")
    with pytest.raises(ReglaDeNegocioError):
        p.aprobar()


def test_specification_beneficio_vip():
    ctx = ContextoPedido(VIP, [Linea("P1", 1, Decimal("1500"))])
    assert APLICA_BENEFICIO.is_satisfied_by(ctx)


def test_specification_beneficio_no_aplica_con_promocion_o_sin_vip():
    lineas = [Linea("P1", 1, Decimal("1500"))]
    assert not APLICA_BENEFICIO.is_satisfied_by(ContextoPedido(VIP, lineas, promocion_activa=True))
    assert not APLICA_BENEFICIO.is_satisfied_by(ContextoPedido(ACTIVO, lineas))
    assert not APLICA_BENEFICIO.is_satisfied_by(
        ContextoPedido(VIP, [Linea("P1", 1, Decimal("1499"))]))


def test_specification_or_y_not():
    ctx = ContextoPedido(ACTIVO, LINEAS)
    assert (EsVipSpec() | TotalMinimoSpec(100)).is_satisfied_by(ctx)
    assert (~PromocionActivaSpec()).is_satisfied_by(ctx)