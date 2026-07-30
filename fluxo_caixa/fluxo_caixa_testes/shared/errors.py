from fastapi import Request
from fastapi.responses import JSONResponse

async def unhandled_exception_handler(request: Request, exc: Exception):
    # Never expose stack traces or database details to clients.
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno. Consulte o identificador da requisição."},
    )
