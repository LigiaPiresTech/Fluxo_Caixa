from fastapi.testclient import TestClient
from api_usuarios.handler import app as usuarios_app
from api_cadastros.handler import app as cadastros_app
from api_contas.handler import app as contas_app
from api_lancamentos.handler import app as lancamentos_app
from api_consolidado.handler import app as consolidado_app
from api_relatorios.handler import app as relatorios_app


def test_all_six_health_endpoints():
    apps = [
        (usuarios_app, "api_usuarios"),
        (cadastros_app, "api_cadastros"),
        (contas_app, "api_contas"),
        (lancamentos_app, "api_lancamentos"),
        (consolidado_app, "api_consolidado"),
        (relatorios_app, "api_relatorios"),
    ]
    for app, expected_service in apps:
        response = TestClient(app).get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["service"] == expected_service


def test_request_id_is_propagated():
    response = TestClient(usuarios_app).get("/health", headers={"X-Request-ID": "req-test-001"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "req-test-001"
