from datetime import date
from types import SimpleNamespace
from fastapi.testclient import TestClient
from api_relatorios.handler import app, get_db

class Query:
    def filter(self, *args, **kwargs): return self
    def group_by(self, *args, **kwargs): return self
    def order_by(self, *args, **kwargs): return self
    def all(self):
        return [SimpleNamespace(data=date(2026,7,30), creditos=1000, debitos=400)]
class DB:
    def query(self, *args, **kwargs): return Query()


def test_cash_flow_returns_daily_credit_debit_and_balance():
    app.dependency_overrides[get_db] = lambda: DB()
    try:
        r = TestClient(app).get("/fluxo-caixa", params={"data_inicio":"2026-07-01","data_fim":"2026-07-31"})
        assert r.status_code == 200
        assert r.json()[0]["saldo_dia"] == 600
    finally: app.dependency_overrides.clear()
