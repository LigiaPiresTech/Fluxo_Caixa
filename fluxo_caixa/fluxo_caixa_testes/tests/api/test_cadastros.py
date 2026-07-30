from types import SimpleNamespace
from fastapi.testclient import TestClient
from api_cadastros.handler import app, get_db

class DB:
    def __init__(self, found=True): self.found = found
    def add(self, obj): obj.id_cliente = 10; obj.id_fornecedor = 20
    def commit(self): pass
    def refresh(self, obj): pass
    def get(self, model, ident):
        if not self.found: return None
        return SimpleNamespace(id_cliente=ident, id_fornecedor=ident, nome_razao_social="ACME", tipo_pessoa="JURIDICA")


def test_create_client():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).post("/clientes", json={"nome_razao_social":"ACME", "tipo_pessoa":"JURIDICA"})
        assert r.status_code == 201
        assert r.json()["id_cliente"] == 10
    finally: app.dependency_overrides.clear()


def test_get_missing_client():
    app.dependency_overrides[get_db] = lambda: DB(found=False)
    try:
        r = TestClient(app).get("/clientes/999")
        assert r.status_code == 404
    finally: app.dependency_overrides.clear()


def test_create_supplier():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).post("/fornecedores", json={"nome_razao_social":"Fornecedor X", "tipo_pessoa":"JURIDICA"})
        assert r.status_code == 201
        assert r.json()["id_fornecedor"] == 20
    finally: app.dependency_overrides.clear()
