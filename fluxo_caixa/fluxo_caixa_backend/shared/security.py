from fastapi import Header, HTTPException, status
from typing import Optional

def claims_from_api_gateway_context(
    x_amzn_apigateway_authorizer: Optional[str] = Header(default=None)
):
    """
    In production, API Gateway HTTP API JWT Authorizer validates the Cognito
    access token before Lambda is invoked. The Lambda receives validated claims
    in requestContext.authorizer.jwt.claims.

    This dependency is intentionally defensive. The production integration
    should pass the claims into the application context.
    """
    if not x_amzn_apigateway_authorizer:
        # Local development only. Do not disable authentication in production.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identidade não fornecida"
        )
    return x_amzn_apigateway_authorizer

def require_scope(claims: dict, required_scope: str):
    scopes = set((claims.get("scope") or "").split())
    if required_scope not in scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
