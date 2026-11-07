from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)
BUEN_PEDIDO = {"cliente_id": "PED-C001", "lineas": [{"recurso_id": "PED-P001", "cantidad": 2}]}


def _crear():
    r = client.post("/pedidos", json=BUEN_PEDIDO)
    assert r.status_code == 201
    return r.json()


def _accion(pid, accion, **extra):
    return client.post(f"/pedidos/{pid}/acciones", json={"accion": accion, **extra})


def test_crear_y_consultar_pedido():
    p = _crear()
    r = client.get(f"/pedidos/{p['id']}")
    assert r.status_code == 200
    assert r.json()["estado"] == "CREADO"
    assert r.json()["total"] == 580.0


def test_pedido_inexistente_404():
    assert client.get("/pedidos/NO-EXISTE").status_code == 404


def test_cliente_inexistente_404():
    body = {**BUEN_PEDIDO, "cliente_id": "NO-EXISTE"}
    assert client.post("/pedidos", json=body).status_code == 404


def test_cliente_inactivo_409():
    body = {**BUEN_PEDIDO, "cliente_id": "PED-C007"}
    assert client.post("/pedidos", json=body).status_code == 409


def test_producto_deshabilitado_409():
    body = {**BUEN_PEDIDO, "lineas": [{"recurso_id": "PED-P011", "cantidad": 1}]}
    assert client.post("/pedidos", json=body).status_code == 409


def test_flujo_completo_persistido():
    pid = _crear()["id"]
    for accion, estado in [("aprobar", "CONFIRMADO"), ("preparar", "EN_PREPARACION"),
                           ("listo", "LISTO"), ("completar", "ENTREGADO")]:
        r = _accion(pid, accion)
        assert r.status_code == 200
        assert r.json()["estado"] == estado
    assert client.get(f"/pedidos/{pid}").json()["estado"] == "ENTREGADO"


def test_transicion_invalida_409():
    pid = _crear()["id"]
    assert _accion(pid, "completar").status_code == 409


def test_accion_invalida_422():
    pid = _crear()["id"]
    assert _accion(pid, "volar").status_code == 422


def test_cancelar_en_preparacion_requiere_autorizacion():
    pid = _crear()["id"]
    _accion(pid, "aprobar")
    _accion(pid, "preparar")
    assert _accion(pid, "cancelar", motivo="Se fue").status_code == 409
    r = _accion(pid, "cancelar", motivo="Se fue", autorizado_por_encargado=True)
    assert r.status_code == 200
    assert r.json()["estado"] == "CANCELADO"


def test_beneficio_vip():
    body = {"cliente_id": "PED-C005",
            "lineas": [{"recurso_id": "PED-P018", "cantidad": 2}]}
    pid = client.post("/pedidos", json=body).json()["id"]
    assert client.get(f"/pedidos/{pid}/beneficio").json()["aplica_beneficio"] is True


def test_beneficio_no_aplica_con_promocion():
    body = {"cliente_id": "PED-C005", "promocion_activa": True,
            "lineas": [{"recurso_id": "PED-P018", "cantidad": 2}]}
    pid = client.post("/pedidos", json=body).json()["id"]
    assert client.get(f"/pedidos/{pid}/beneficio").json()["aplica_beneficio"] is False