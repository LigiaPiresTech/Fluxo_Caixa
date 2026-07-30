from types import SimpleNamespace
from fastapi.testclient import TestClient
from api_usuarios.handler import app, get_db


def fake_db(existing=None):
    class Query:
        def filter(self, *args, **kwargs): return self
        def first(self): return existing
    class DB:
        def query(self, *args, **kwargs): return Query()
        def add(self, obj): obj.id_usuario = 101; obj.ativo = True
        def commit(self): pass
        def refresh(self, obj): pass
        def get(self, model, ident): return SimpleNamespace(
            id_usuario=ident, id_perfil=1, cognito_sub="sub", nome="Maria", email="maria@example.com", cpf=None, telefone=None, ativo=True
        ) if ident == 101 else None
    return DB()


def test_create_user_returns_201(monkeypatch):
    db = fake_db()
    app.dependency_overrides[get_db] = lambda: db
    try:
        response = TestClient(app).post("/usuarios", json={
            "id_perfil": 1, "cognito_sub": "sub-101", "nome": "Maria Silva", "email": "maria@example.com"
        })
        assert response.status_code == 201
        assert response.json()["id_usuario"] == 101
    finally:
        app.dependency_overrides.clear()


def test_duplicate_user_returns_409():
    existing = object()
    db = fake_db(existing=existing)
    app.dependency_overrides[get_db] = lambda: db
    try:
        response = TestClient(app).post("/usuarios", json={
            "id_perfil": 1, "cognito_sub": "sub-101", "nome": "Maria Silva", "email": "maria@example.com"
        })
        assert response.status_code == 409
    finally:
        app.dependency_overrides.clear()


def test_get_unknown_user_returns_404():
    db = fake_db()
    app.dependency_overrides[get_db] = lambda: db
    try:
        response = TestClient(app).get("/usuarios/999")
        assert response.status_code == 404
    finally:
        app.dependency_overrides.clear()
