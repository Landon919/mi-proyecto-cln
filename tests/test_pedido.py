from fastapi.testclient import TestClient
from src.api.main import app
from src.infrastructure.repositories import db_en_memoria

client = TestClient(app)

def test_crear_pedido_y_transicion_estado():
    # 1. Inyectamos un dato de prueba forzado en memoria para pasar la validación Specification
    db_en_memoria.actores["PED-C001"] = {"actor_id": "PED-C001", "activo": 1}
    
    # 2. Probar Crear Pedido (Integra la API con los servicios y reglas)
    response = client.post("/pedidos/", json={
        "actor_id": "PED-C001",
        "lineas": [{"recurso_id": "PED-P001", "cantidad": 2}]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["estado"] == "CREADO"
    pedido_id = data["pedido_id"]

    # 3. Probar State Machine (Transición Válida: CREADO -> CONFIRMADO)
    resp_estado = client.patch(f"/pedidos/{pedido_id}/estado?nuevo_estado=CONFIRMADO")
    assert resp_estado.status_code == 200
    assert resp_estado.json()["estado"] == "CONFIRMADO"

    # 4. Probar State Machine (Transición Inválida: CONFIRMADO -> ENTREGADO)
    resp_invalida = client.patch(f"/pedidos/{pedido_id}/estado?nuevo_estado=ENTREGADO")
    assert resp_invalida.status_code == 400