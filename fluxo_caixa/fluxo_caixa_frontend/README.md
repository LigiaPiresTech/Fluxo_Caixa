# Front-end React — Sistema de Fluxo de Caixa

Front-end corporativo em React/Vite preparado para:

React → CloudFront/S3 → API Gateway → Cognito → 6 APIs Lambda.

## Serviços

- Usuários
- Cadastros
- Contas Financeiras
- Lançamentos
- Consolidado
- Relatórios

## Segurança

- Amazon Cognito para autenticação.
- Access token JWT enviado no header Authorization.
- API Gateway deve validar o JWT antes da Lambda.
- CORS restritivo em produção.
- HTTPS obrigatório.
- Nenhum segredo AWS é armazenado no código.
- Variáveis de ambiente apenas para IDs/configuração pública do front.
- O front não acessa RDS diretamente.

## Deploy AWS

O build pode ser publicado em um bucket S3 privado e servido por CloudFront com Origin Access Control (OAC).

Fluxo:

Browser
  ↓ HTTPS
CloudFront
  ↓
S3
  ↓
Cognito para login
  ↓ JWT
API Gateway
  ↓
6 Lambdas

## Instalação

npm install
cp .env.example .env
npm run dev

Para produção:

npm run build

O diretório dist/ é o artefato para o S3/CloudFront.

## Observação

As URLs do API Gateway e os IDs do Cognito no .env.example são placeholders. Devem ser substituídos pelos valores reais do ambiente.
