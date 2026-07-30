# Backend — Sistema de Fluxo de Caixa:

Backend de referência em Python/FastAPI, preparado para AWS Lambda + API Gateway + Cognito + RDS Proxy + PostgreSQL.

## 6 APIs

1. API Usuários
2. API Cadastros
3. API Contas Financeiras
4. API Lançamentos
5. API Consolidado
6. API Relatórios

## Arquitetura

Cliente → API Gateway → JWT Authorizer (Cognito) → Lambda → RDS Proxy → RDS PostgreSQL

O Data Lake não é usado como fonte transacional do saldo. O RDS é a fonte oficial das transações operacionais.

## Segurança

- Cognito + JWT no API Gateway.
- APIs privadas em subnets privadas via Lambda/VPC.
- RDS sem exposição pública.
- RDS Proxy entre Lambda e RDS.
- Segredos fora do código, em Secrets Manager.
- IAM least privilege.
- TLS em trânsito.
- KMS para criptografia em repouso conforme configuração AWS.
- CloudWatch/X-Ray para observabilidade.
- CloudTrail para trilha de auditoria AWS.
- Validação de entrada com Pydantic.
- SQL parametrizado via SQLAlchemy.
- Não retornar stack trace/credenciais ao cliente.

O API Gateway deve validar o JWT antes de encaminhar a requisição para a Lambda. A aplicação não deve reimplementar desnecessariamente a validação criptográfica do JWT.

## Requisito de 50 req/s do Consolidado

Para o cenário de pico, a API de Consolidado deve ser protegida contra sobrecarga e desacoplada do fluxo de lançamento.

Para processamento assíncrono:
EventBridge → SQS → Lambda Consolidado → RDS.

## Importante

O código é um baseline de produção arquitetural, não um sistema pronto para produção sem configuração. Antes do deploy, devem ser definidos:
- IDs de VPC/subnets/security groups;
- Cognito User Pool e App Client;
- scopes/claims e autorização por perfil;
- RDS Proxy;
- Secret do Secrets Manager;
- regras de Security Group;
- limites de concorrência;
- alarmes CloudWatch;
- WAF;
- KMS;
- CI/CD;
- migrações de banco;
- testes unitários/integrados;
- política de DR e RTO/RPO.
