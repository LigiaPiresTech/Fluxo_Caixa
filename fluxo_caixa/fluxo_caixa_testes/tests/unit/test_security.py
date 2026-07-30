import pytest
from fastapi import HTTPException
from shared.security import claims_from_api_gateway_context, require_scope
from api_lancamentos.handler import current_user_id


def test_missing_api_gateway_identity_is_rejected():
    with pytest.raises(HTTPException) as exc:
        claims_from_api_gateway_context(None)
    assert exc.value.status_code == 401


def test_scope_is_required():
    with pytest.raises(HTTPException) as exc:
        require_scope({"scope": "relatorios:read"}, "lancamentos:write")
    assert exc.value.status_code == 403


def test_required_scope_is_accepted():
    claims = {"scope": "lancamentos:write relatorios:read"}
    assert require_scope(claims, "lancamentos:write") is None


def test_launch_requires_user_identity():
    with pytest.raises(HTTPException) as exc:
        current_user_id(None)
    assert exc.value.status_code == 401


def test_launch_rejects_invalid_user_identity():
    with pytest.raises(HTTPException) as exc:
        current_user_id("abc")
    assert exc.value.status_code == 401


def test_launch_accepts_numeric_user_identity():
    assert current_user_id("123") == 123
