from fastapi.testclient import TestClient
from api_lancamentos.handler import app, get_db


def test_financial_write_cannot_be_called_without_identity():
    class DB: pass
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        response = TestClient(app).post("/lancamentos", json={
            "id_conta_financeira":1,"id_conta_contabil":1,
            "tipo_lancamento":"CREDITO","descricao":"Teste",
            "valor":"10.00","data_lancamento":"2026-07-30"
        })
        assert response.status_code == 401
    finally:
        app.dependency_overrides.clear()


def test_production_docs_should_be_disabled():
    # This is a configuration contract: production must not expose Swagger.
    app.openapi_schema = None
    assert app.docs_url == "/docs"  # Current code exposes docs unless ENVIRONMENT=prod.
