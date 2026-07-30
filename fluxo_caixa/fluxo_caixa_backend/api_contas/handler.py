from mangum import Mangum
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from shared.app import create_app
from shared.db import get_db
from shared.entities import ContaFinanceira
from shared.schemas import AccountCreate

app = create_app("API Contas Financeiras")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_contas"}

@app.post("/contas-financeiras", status_code=201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    obj = ContaFinanceira(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/contas-financeiras/{id_conta_financeira}")
def get_account(id_conta_financeira: int, db: Session = Depends(get_db)):
    obj = db.get(ContaFinanceira, id_conta_financeira)
    if not obj:
        raise HTTPException(status_code=404, detail="Conta financeira não encontrada")
    return obj

handler = Mangum(app)
