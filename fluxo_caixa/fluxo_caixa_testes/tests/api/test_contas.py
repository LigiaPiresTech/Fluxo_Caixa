from types import SimpleNamespace
from fastapi.testclient import TestClient
from api_contas.handler import app, get_db

class DB:
    def __init__(self, found=True): self.found = found
    def add(self, obj): obj.id_conta_financeira = 7; obj.ativo = True
    def commit(self): pass
    def refresh(self, obj): pass
    def get(self, model, ident):
        if not self.found: return None
        return SimpleNamespace(id_conta_financeira=ident, id_tipo_conta=1, nome="Conta Principal", banco="Banco X", agencia="1", numero_conta="123", digito_conta="0", saldo_inicial=0, data_saldo_inicial=None, ativo=True)


def test_create_account():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).post("/contas-financeiras", json={"id_tipo_conta":1,"nome":"Conta Principal","saldo_inicial":"1000.00"})
        assert r.status_code == 201
        assert r.json()["id_conta_financeira"] == 7
    finally: app.dependency_overrides.clear()


def test_get_missing_account():
    app.dependency_overrides[get_db] = lambda: DB(found=False)
    try:
        r = TestClient(app).get("/contas-financeiras/999")
        assert r.status_code == 404
    finally: app.dependency_overrides.clear()
