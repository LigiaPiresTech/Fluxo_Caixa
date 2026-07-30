from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
from fastapi.testclient import TestClient
from api_lancamentos.handler import app, get_db

PAYLOAD = {
    "id_conta_financeira": 1, "id_conta_contabil": 1,
    "tipo_lancamento": "DEBITO", "descricao": "Despesa operacional",
    "valor": "250.00", "data_lancamento": "2026-07-30", "status": "CONFIRMADO"
}

class DB:
    def add(self, obj):
        obj.id_lancamento = 500
    def commit(self): pass
    def refresh(self, obj): pass
    def get(self, model, ident):
        if ident != 500: return None
        return SimpleNamespace(**PAYLOAD, id_lancamento=500, id_usuario_criacao=99, data_criacao=datetime(2026,7,30))


def test_create_launch_requires_identity():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).post("/lancamentos", json=PAYLOAD)
        assert r.status_code == 401
    finally: app.dependency_overrides.clear()


def test_create_launch_returns_201_and_user():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).post("/lancamentos", json=PAYLOAD, headers={"X-User-ID":"99"})
        assert r.status_code == 201
        assert r.json()["id_usuario_criacao"] == 99
        assert r.json()["valor"] == "250.00"
    finally: app.dependency_overrides.clear()


def test_create_launch_rejects_negative_amount():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        bad = {**PAYLOAD, "valor": "-1.00"}
        r = TestClient(app).post("/lancamentos", json=bad, headers={"X-User-ID":"99"})
        assert r.status_code == 422
    finally: app.dependency_overrides.clear()


def test_get_unknown_launch_returns_404():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).get("/lancamentos/999")
        assert r.status_code == 404
    finally: app.dependency_overrides.clear()
