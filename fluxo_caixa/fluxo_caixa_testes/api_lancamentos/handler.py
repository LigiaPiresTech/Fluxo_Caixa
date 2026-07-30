from datetime import datetime, timezone
from mangum import Mangum
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from shared.app import create_app
from shared.db import get_db
from shared.entities import Lancamento
from shared.schemas import LaunchCreate, LaunchOut
from shared.audit import audit_event

app = create_app("API Lançamentos")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_lancamentos"}

def current_user_id(x_user_id: str | None = Header(default=None)) -> int:
    # In production, API Gateway/Cognito claims should be mapped to this value.
    # Never trust a client-provided user ID directly.
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Usuário não autenticado")
    try:
        return int(x_user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Identidade inválida")

@app.post("/lancamentos", response_model=LaunchOut, status_code=201)
def create_launch(
    payload: LaunchCreate,
    user_id: int = Depends(current_user_id),
    db: Session = Depends(get_db),
):
    # Financial writes are transactional. All SQL is generated through SQLAlchemy
    # parameters, avoiding string concatenation/SQL injection.
    obj = Lancamento(
        **payload.model_dump(),
        id_usuario_criacao=user_id,
        data_criacao=datetime.now(timezone.utc),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    audit_event(
        "FINANCIAL_LAUNCH_CREATED",
        str(user_id),
        "LANCAMENTO",
        str(obj.id_lancamento),
        "CREATE",
        {"tipo": obj.tipo_lancamento, "valor": str(obj.valor)}
    )
    return obj

@app.get("/lancamentos/{id_lancamento}", response_model=LaunchOut)
def get_launch(id_lancamento: int, db: Session = Depends(get_db)):
    obj = db.get(Lancamento, id_lancamento)
    if not obj:
        raise HTTPException(status_code=404, detail="Lançamento não encontrado")
    return obj

handler = Mangum(app)
