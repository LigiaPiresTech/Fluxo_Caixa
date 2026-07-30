from datetime import date
from decimal import Decimal
import pytest
from pydantic import ValidationError
from shared.schemas import UserCreate, ClientCreate, AccountCreate, LaunchCreate, ReportFilter


def valid_launch(**overrides):
    data = {
        "id_conta_financeira": 1,
        "id_conta_contabil": 1,
        "tipo_lancamento": "CREDITO",
        "descricao": "Recebimento cliente",
        "valor": Decimal("1500.00"),
        "data_lancamento": date(2026, 7, 30),
    }
    data.update(overrides)
    return data


def test_user_valid_email():
    obj = UserCreate(id_perfil=1, cognito_sub="sub-1", nome="Maria Silva", email="maria@example.com")
    assert obj.email == "maria@example.com"


def test_user_invalid_email_rejected():
    with pytest.raises(ValidationError):
        UserCreate(id_perfil=1, cognito_sub="sub-1", nome="Maria Silva", email="email-invalido")


def test_client_person_type_is_restricted():
    with pytest.raises(ValidationError):
        ClientCreate(nome_razao_social="Cliente X", tipo_pessoa="INVALIDA")


@pytest.mark.parametrize("tipo", ["CREDITO", "DEBITO"])
def test_launch_accepts_credit_or_debit(tipo):
    obj = LaunchCreate(**valid_launch(tipo_lancamento=tipo))
    assert obj.tipo_lancamento == tipo


def test_launch_rejects_zero_or_negative_value():
    for value in [Decimal("0"), Decimal("-1")]:
        with pytest.raises(ValidationError):
            LaunchCreate(**valid_launch(valor=value))


def test_launch_rejects_more_than_two_decimal_places():
    with pytest.raises(ValidationError):
        LaunchCreate(**valid_launch(valor=Decimal("10.999")))


def test_report_filter_requires_date_range():
    obj = ReportFilter(data_inicio=date(2026, 7, 1), data_fim=date(2026, 7, 31))
    assert obj.data_inicio < obj.data_fim
