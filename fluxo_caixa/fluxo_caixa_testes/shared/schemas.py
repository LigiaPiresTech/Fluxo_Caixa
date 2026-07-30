from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Optional, Literal

class UserCreate(BaseModel):
    id_perfil: int
    cognito_sub: str = Field(min_length=1, max_length=255)
    nome: str = Field(min_length=2, max_length=150)
    email: EmailStr
    cpf: Optional[str] = None
    telefone: Optional[str] = None

class UserOut(UserCreate):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: int
    ativo: bool

class GenericStatus(BaseModel):
    ativo: bool = True

class ClientCreate(BaseModel):
    nome_razao_social: str = Field(min_length=2, max_length=200)
    tipo_pessoa: Literal["FISICA", "JURIDICA"]
    cpf_cnpj: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = Field(default=None, min_length=2, max_length=2)
    cep: Optional[str] = None

class SupplierCreate(ClientCreate):
    pass

class AccountCreate(BaseModel):
    id_tipo_conta: int
    nome: str = Field(min_length=2, max_length=150)
    banco: Optional[str] = None
    agencia: Optional[str] = None
    numero_conta: Optional[str] = None
    digito_conta: Optional[str] = None
    saldo_inicial: Decimal = Decimal("0")
    data_saldo_inicial: Optional[date] = None

class LaunchCreate(BaseModel):
    id_conta_financeira: int
    id_conta_contabil: int
    id_centro_custo: Optional[int] = None
    id_cliente: Optional[int] = None
    id_fornecedor: Optional[int] = None
    id_produto: Optional[int] = None
    id_servico: Optional[int] = None
    id_forma_pagamento: Optional[int] = None
    tipo_lancamento: Literal["CREDITO", "DEBITO"]
    descricao: str = Field(min_length=2, max_length=500)
    valor: Decimal = Field(gt=0, max_digits=15, decimal_places=2)
    data_lancamento: date
    data_competencia: Optional[date] = None
    data_vencimento: Optional[date] = None
    data_pagamento: Optional[date] = None
    status: Literal["PENDENTE", "CONFIRMADO", "CANCELADO", "ESTORNADO"] = "PENDENTE"
    numero_documento: Optional[str] = None
    observacao: Optional[str] = None

class LaunchOut(LaunchCreate):
    model_config = ConfigDict(from_attributes=True)
    id_lancamento: int
    id_usuario_criacao: int
    data_criacao: datetime

class ConsolidatedBalance(BaseModel):
    id_conta_financeira: int
    data_inicio: date
    data_fim: date
    total_creditos: Decimal
    total_debitos: Decimal
    saldo: Decimal
    quantidade_lancamentos: int

class ReportFilter(BaseModel):
    data_inicio: date
    data_fim: date
    id_conta_financeira: Optional[int] = None
    id_centro_custo: Optional[int] = None
