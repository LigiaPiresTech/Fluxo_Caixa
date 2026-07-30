from datetime import date
from decimal import Decimal
from mangum import Mangum
from fastapi import Depends, Query
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from shared.app import create_app
from shared.db import get_db
from shared.entities import Lancamento
from shared.schemas import ConsolidatedBalance

app = create_app("API Consolidado")

@app.get("/health")
def health():
    return {"status": "ok", "service": "api_consolidado"}

@app.get("/saldo", response_model=ConsolidatedBalance)
def consolidated_balance(
    id_conta_financeira: int,
    data_inicio: date,
    data_fim: date,
    db: Session = Depends(get_db),
):
    credit = func.coalesce(func.sum(
        case((Lancamento.tipo_lancamento == "CREDITO", Lancamento.valor), else_=0)
    ), 0)
    debit = func.coalesce(func.sum(
        case((Lancamento.tipo_lancamento == "DEBITO", Lancamento.valor), else_=0)
    ), 0)

    row = db.query(
        credit.label("creditos"),
        debit.label("debitos"),
        func.count(Lancamento.id_lancamento).label("quantidade"),
    ).filter(
        Lancamento.id_conta_financeira == id_conta_financeira,
        Lancamento.data_lancamento >= data_inicio,
        Lancamento.data_lancamento <= data_fim,
        Lancamento.status == "CONFIRMADO",
    ).one()

    total_creditos = Decimal(str(row.creditos or 0))
    total_debitos = Decimal(str(row.debitos or 0))

    return ConsolidatedBalance(
        id_conta_financeira=id_conta_financeira,
        data_inicio=data_inicio,
        data_fim=data_fim,
        total_creditos=total_creditos,
        total_debitos=total_debitos,
        saldo=total_creditos-total_debitos,
        quantidade_lancamentos=row.quantidade,
    )

handler = Mangum(app)
