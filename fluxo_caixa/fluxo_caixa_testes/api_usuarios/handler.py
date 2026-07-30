from mangum import Mangum
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from shared.app import create_app
from shared.db import get_db
from shared.entities import Usuario
from shared.schemas import UserCreate, UserOut
from shared.audit import audit_event

app = create_app("API Usuários")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_usuarios"}

@app.post("/usuarios", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(Usuario).filter(
        (Usuario.email == payload.email) | (Usuario.cognito_sub == payload.cognito_sub)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Usuário já cadastrado")

    user = Usuario(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    audit_event("USER_CREATED", str(user.id_usuario), "USUARIO",
                str(user.id_usuario), "CREATE")
    return user

@app.get("/usuarios/{id_usuario}", response_model=UserOut)
def get_user(id_usuario: int, db: Session = Depends(get_db)):
    user = db.get(Usuario, id_usuario)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

handler = Mangum(app)
