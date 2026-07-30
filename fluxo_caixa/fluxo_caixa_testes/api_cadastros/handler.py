from mangum import Mangum
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from shared.app import create_app
from shared.db import get_db
from shared.entities import Cliente, Fornecedor
from shared.schemas import ClientCreate, SupplierCreate

app = create_app("API Cadastros")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_cadastros"}

@app.post("/clientes", status_code=201)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    obj = Cliente(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"id_cliente": obj.id_cliente, "nome_razao_social": obj.nome_razao_social}

@app.get("/clientes/{id_cliente}")
def get_client(id_cliente: int, db: Session = Depends(get_db)):
    obj = db.get(Cliente, id_cliente)
    if not obj:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return obj

@app.post("/fornecedores", status_code=201)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    obj = Fornecedor(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"id_fornecedor": obj.id_fornecedor, "nome_razao_social": obj.nome_razao_social}

@app.get("/fornecedores/{id_fornecedor}")
def get_supplier(id_fornecedor: int, db: Session = Depends(get_db)):
    obj = db.get(Fornecedor, id_fornecedor)
    if not obj:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return obj

handler = Mangum(app)
