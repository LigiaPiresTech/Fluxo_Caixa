from fastapi.testclient import TestClient
from api_usuarios.handler import app as usuarios
from api_cadastros.handler import app as cadastros
from api_contas.handler import app as contas
from api_lancamentos.handler import app as lancamentos
from api_consolidado.handler import app as consolidado
from api_relatorios.handler import app as relatorios


def test_openapi_exposes_expected_api_surface():
    expected = {
        "usuarios": ["/health", "/usuarios", "/usuarios/{id_usuario}"],
        "cadastros": ["/health", "/clientes", "/clientes/{id_cliente}", "/fornecedores", "/fornecedores/{id_fornecedor}"],
        "contas": ["/health", "/contas-financeiras", "/contas-financeiras/{id_conta_financeira}"],
        "lancamentos": ["/health", "/lancamentos", "/lancamentos/{id_lancamento}"],
        "consolidado": ["/health", "/saldo"],
        "relatorios": ["/health", "/fluxo-caixa"],
    }
    apps = {"usuarios": usuarios, "cadastros": cadastros, "contas": contas, "lancamentos": lancamentos, "consolidado": consolidado, "relatorios": relatorios}
    for name, paths in expected.items():
        schema = apps[name].openapi()
        for path in paths:
            assert path in schema["paths"], f"{name}: endpoint ausente: {path}"
