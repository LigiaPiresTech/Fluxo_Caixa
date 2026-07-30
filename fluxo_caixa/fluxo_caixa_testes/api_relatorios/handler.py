from datetime import date
from mangum import Mangum
from fastapi import Depends
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from shared.app import create_app
from shared.db import get_db
from shared.entities import Lancamento

app = create_app("API Relatórios")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_relatorios"}

@app.get("/fluxo-caixa")
def cash_flow(
    data_inicio: date,
    data_fim: date,
    id_conta_financeira: int | None = None,
    id_centro_custo: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(
        Lancamento.data_lancamento.label("data"),
        func.coalesce(func.sum(
            case((Lancamento.tipo_lancamento == "CREDITO", Lancamento.valor), else_=0)
        ), 0).label("creditos"),
        func.coalesce(func.sum(
            case((Lancamento.tipo_lancamento == "DEBITO", Lancamento.valor), else_=0)
        ), 0).label("debitos"),
    ).filter(
        Lancamento.data_lancamento >= data_inicio,
        Lancamento.data_lancamento <= data_fim,
        Lancamento.status == "CONFIRMADO",
    )

    if id_conta_financeira:
        query = query.filter(Lancamento.id_conta_financeira == id_conta_financeira)
    if id_centro_custo:
        query = query.filter(Lancamento.id_centro_custo == id_centro_custo)

    rows = query.group_by(Lancamento.data_lancamento).order_by(Lancamento.data_lancamento).all()

    return [
        {
            "data": row.data,
            "creditos": row.creditos,
            "debitos": row.debitos,
            "saldo_dia": row.creditos - row.debitos,
        }
        for row in rows
    ]

handler = Mangum(app)
