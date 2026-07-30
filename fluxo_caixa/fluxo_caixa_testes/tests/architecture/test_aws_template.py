from pathlib import Path
import re
import pytest

TEMPLATE = Path(__file__).parents[2] / "template.yaml"


def read_template():
    return TEMPLATE.read_text(encoding="utf-8")


def test_template_defines_six_lambda_services():
    text = read_template()
    for name in [
        "UsuariosFunction", "CadastrosFunction", "ContasFunction",
        "LancamentosFunction", "ConsolidadoFunction", "RelatoriosFunction"
    ]:
        assert name in text


def test_api_uses_cognito_jwt_authorizer():
    text = read_template()
    assert "CognitoJwt:" in text
    assert "JwtConfiguration:" in text
    assert "DefaultAuthorizer: CognitoJwt" in text


def test_lambda_tracing_is_active():
    assert "Tracing: Active" in read_template()


def test_database_secret_is_used():
    text = read_template()
    assert "DatabaseUrlSecretArn" in text
    assert "AWSSecretsManagerGetSecretValuePolicy" in text


@pytest.mark.xfail(reason="Infraestrutura AWS ainda não criada no projeto: WAF/KMS/CloudTrail/GuardDuty/Security Hub serão implementados no IaC.")
def test_security_services_required_by_case_are_in_iac():
    text = read_template()
    for service in ["WAF", "KMS", "CloudTrail", "GuardDuty", "SecurityHub"]:
        assert service.lower() in text.lower()


@pytest.mark.xfail(reason="A versão atual do backend ainda não implementa EventBridge/SQS para o desacoplamento de Lançamentos e Consolidado.")
def test_async_messaging_is_present_for_launches():
    text = read_template().lower()
    assert "sqs" in text
    assert "eventbridge" in text


@pytest.mark.xfail(reason="Idempotência ainda precisa ser implementada no serviço de Lançamentos.")
def test_launches_have_idempotency_contract():
    text = read_template().lower()
    assert "idempotency" in text
