from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .models import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_perfil: Mapped[int] = mapped_column(ForeignKey("perfil_usuario.id_perfil"))
    cognito_sub: Mapped[str] = mapped_column(String(255), unique=True)
    nome: Mapped[str] = mapped_column(String(150))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    cpf: Mapped[str | None] = mapped_column(String(14))
    telefone: Mapped[str | None] = mapped_column(String(20))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nome_razao_social: Mapped[str] = mapped_column(String(200))
    tipo_pessoa: Mapped[str] = mapped_column(String(20))
    cpf_cnpj: Mapped[str | None] = mapped_column(String(18))
    email: Mapped[str | None] = mapped_column(String(255))
    telefone: Mapped[str | None] = mapped_column(String(20))
    endereco: Mapped[str | None] = mapped_column(String(300))
    cidade: Mapped[str | None] = mapped_column(String(100))
    uf: Mapped[str | None] = mapped_column(String(2))
    cep: Mapped[str | None] = mapped_column(String(10))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id_fornecedor: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nome_razao_social: Mapped[str] = mapped_column(String(200))
    tipo_pessoa: Mapped[str] = mapped_column(String(20))
    cpf_cnpj: Mapped[str | None] = mapped_column(String(18))
    email: Mapped[str | None] = mapped_column(String(255))
    telefone: Mapped[str | None] = mapped_column(String(20))
    endereco: Mapped[str | None] = mapped_column(String(300))
    cidade: Mapped[str | None] = mapped_column(String(100))
    uf: Mapped[str | None] = mapped_column(String(2))
    cep: Mapped[str | None] = mapped_column(String(10))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

class ContaFinanceira(Base):
    __tablename__ = "conta_financeira"
    id_conta_financeira: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_tipo_conta: Mapped[int] = mapped_column(ForeignKey("tipo_conta.id_tipo_conta"))
    nome: Mapped[str] = mapped_column(String(150))
    banco: Mapped[str | None] = mapped_column(String(100))
    agencia: Mapped[str | None] = mapped_column(String(20))
    numero_conta: Mapped[str | None] = mapped_column(String(30))
    digito_conta: Mapped[str | None] = mapped_column(String(5))
    saldo_inicial: Mapped[object] = mapped_column(Numeric(15,2), default=0)
    data_saldo_inicial: Mapped[Date | None] = mapped_column(Date)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

class Lancamento(Base):
    __tablename__ = "lancamentos"
    id_lancamento: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    id_conta_financeira: Mapped[int] = mapped_column(ForeignKey("conta_financeira.id_conta_financeira"))
    id_conta_contabil: Mapped[int] = mapped_column(ForeignKey("contas_contabeis.id_conta_contabil"))
    id_centro_custo: Mapped[int | None] = mapped_column(BigInteger)
    id_cliente: Mapped[int | None] = mapped_column(BigInteger)
    id_fornecedor: Mapped[int | None] = mapped_column(BigInteger)
    id_produto: Mapped[int | None] = mapped_column(BigInteger)
    id_servico: Mapped[int | None] = mapped_column(BigInteger)
    id_forma_pagamento: Mapped[int | None] = mapped_column(BigInteger)
    tipo_lancamento: Mapped[str] = mapped_column(String(10))
    descricao: Mapped[str] = mapped_column(String(500))
    valor: Mapped[object] = mapped_column(Numeric(15,2))
    data_lancamento: Mapped[Date] = mapped_column(Date)
    data_competencia: Mapped[Date | None] = mapped_column(Date)
    data_vencimento: Mapped[Date | None] = mapped_column(Date)
    data_pagamento: Mapped[Date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20))
    numero_documento: Mapped[str | None] = mapped_column(String(100))
    observacao: Mapped[str | None] = mapped_column(String(1000))
    id_usuario_criacao: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    data_criacao: Mapped[DateTime] = mapped_column(DateTime)
    data_atualizacao: Mapped[DateTime | None] = mapped_column(DateTime)
