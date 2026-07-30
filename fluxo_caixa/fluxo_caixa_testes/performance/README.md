# Teste de carga do case

O case exige pico de aproximadamente 50 requisições/segundo no Consolidado Diário e admite no máximo 5% de perda. O teste deve ser executado contra um ambiente não produtivo, preferencialmente homologação, usando o endpoint real do API Gateway.

Exemplo:

```bash
export ACCESS_TOKEN="<JWT_DE_TESTE>"
export ACCOUNT_ID="1"
locust -f performance/locustfile.py --host=https://<api-gateway> --headless -u 100 -r 20 -t 5m
```

Critério de aceite recomendado:
- throughput >= 50 RPS no cenário de pico;
- taxa de falha <= 5%;
- p95 de latência definido pelo SLA do negócio;
- nenhuma duplicidade de lançamento;
- nenhuma perda de transação confirmada.
