from types import SimpleNamespace
from fastapi.testclient import TestClient
from api_consolidado.handler import app, get_db

class Query:
    def filter(self, *args, **kwargs): return self
    def one(self): return SimpleNamespace(creditos=1000, debitos=300, quantidade=4)
class DB:
    def query(self, *args, **kwargs): return Query()


def test_consolidated_balance_calculates_net_balance():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).get("/saldo", params={"id_conta_financeira":1,"data_inicio":"2026-07-01","data_fim":"2026-07-31"})
        assert r.status_code == 200
        body = r.json()
        assert body["total_creditos"] == "1000.00"
        assert body["total_debitos"] == "300.00"
        assert body["saldo"] == "700.00"
        assert body["quantidade_lancamentos"] == 4
    finally: app.dependency_overrides.clear()
