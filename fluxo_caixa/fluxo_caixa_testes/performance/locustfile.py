import os
from locust import HttpUser, task, between

TOKEN = os.getenv("ACCESS_TOKEN", "")
ACCOUNT_ID = os.getenv("ACCOUNT_ID", "1")

class FluxoCaixaUser(HttpUser):
    # Keep a small wait so the load profile can reach the case peak of ~50 req/s
    # when the runner is configured with enough users/workers.
    wait_time = between(0.05, 0.2)

    def on_start(self):
        self.headers = {
            "Authorization": f"Bearer {TOKEN}",
            "X-Request-ID": "load-test",
        } if TOKEN else {"X-Request-ID": "load-test"}

    @task(5)
    def consolidated(self):
        self.client.get(
            "/consolidado/saldo",
            params={"id_conta_financeira": ACCOUNT_ID, "data_inicio": "2026-07-01", "data_fim": "2026-07-31"},
            headers=self.headers,
            name="GET /consolidado/saldo",
        )

    @task(2)
    def health(self):
        self.client.get("/consolidado/health", headers=self.headers, name="GET /consolidado/health")

    @task(1)
    def report(self):
        self.client.get(
            "/relatorios/fluxo-caixa",
            params={"data_inicio":"2026-07-01","data_fim":"2026-07-31"},
            headers=self.headers,
            name="GET /relatorios/fluxo-caixa",
        )
