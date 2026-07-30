# Suíte de testes — Sistema Fluxo de Caixa

Esta suíte foi criada para acompanhar o backend Python/FastAPI/Lambda e o frontend React do projeto. Ela cobre testes unitários, validação de contratos, APIs, segurança, carga e smoke test do frontend.

## Cobertura

- 6 APIs: Usuários, Cadastros, Contas, Lançamentos, Consolidado e Relatórios.
- Validação dos schemas financeiros.
- Autenticação/identidade e autorização por escopo.
- Códigos HTTP 201, 401, 403, 404, 409 e 422.
- Cálculo de consolidado e fluxo de caixa.
- Propagação de X-Request-ID.
- Contrato OpenAPI dos endpoints.
- Teste de carga próximo ao requisito de 50 RPS e taxa de erro máxima de 5%.
- Smoke test do frontend.

## Executar testes de backend

A partir desta pasta, instale as dependências do backend e de teste. Em ambiente real, a variável DATABASE_URL dos testes deve apontar para banco de testes ou ser substituída por fixtures de integração; nunca use o RDS de produção.

```bash
pip install -r requirements-test.txt
pytest
pytest --cov=. --cov-report=term-missing
```

## Carga

```bash
export ACCESS_TOKEN="<JWT_DE_TESTE>"
locust -f performance/locustfile.py --host=https://<api-gateway> --headless -u 100 -r 20 -t 5m
```

## Frontend

```bash
cd frontend
npm install
npm test
npm run e2e
```

## Importante sobre o case

Lançamentos permanece disponível quando Consolidado estiver indisponível, com persistência transacional, mensageria assíncrona, retentativas, idempotência e RPO zero para lançamentos. Os testes de resiliência dessa parte devem ser executados contra a infraestrutura AWS implantada, simulando indisponibilidade do consumidor e verificando que os lançamentos continuam sendo persistidos e que as mensagens pendentes são processadas após a recuperação.

A autenticação Cognito/JWT é parcialmente preparada, mas a validação real das claims deve ocorrer no API Gateway e a autorização por perfil/escopo precisa estar integrada aos handlers antes do aceite de produção.
