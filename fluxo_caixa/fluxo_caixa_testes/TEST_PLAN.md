# Plano de testes do case

## 1. Testes unitários

Validam regras isoladas: schemas, valores monetários, tipos de lançamento, identidade e autorização.

## 2. Testes de API/integração

Validam as 6 APIs, códigos HTTP, payloads, filtros, cálculo do saldo e fluxo de caixa.

## 3. Testes de segurança

Validam ausência de identidade, escopo insuficiente, propagação de request ID e contratos de autenticação. A validação criptográfica do JWT Cognito deve ser exercida no API Gateway em homologação.

## 4. Testes de contrato

Validam se os endpoints previstos continuam publicados no OpenAPI.

## 5. Testes de carga

O cenário do case exige aproximadamente 50 RPS no Consolidado e no máximo 5% de perda. O Locust foi incluído para execução contra API Gateway em homologação.

## 6. Testes de resiliência

Devem desligar o consumidor do Consolidado, gerar lançamentos e comprovar que Lançamentos continua operacional e que os eventos pendentes são processados após a recuperação.

## 7. Testes de DR

Devem simular indisponibilidade da região primária e comprovar RPO/RTO. Para Lançamentos, o requisito definido no documento é RPO zero. O RTO precisa ser validado contra o objetivo acordado com o negócio.

## 8. Testes de frontend

Smoke test com Playwright e teste do contrato de sessão Cognito.

## 9. Critérios de aceite

- Todos os testes unitários e de integração verdes.
- Taxa de erro do teste de carga <= 5%.
- Nenhuma transação financeira confirmada perdida.
- Nenhuma duplicidade causada por retry/reenvio.
- Lançamentos continuam disponíveis quando Consolidado está indisponível.
- Logs, métricas e tracing disponíveis.
- Acesso não autorizado retorna 401/403.
- Dados financeiros não são expostos em logs.
