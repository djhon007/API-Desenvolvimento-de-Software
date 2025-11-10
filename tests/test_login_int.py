from fastapi.testclient import TestClient
from main import app # app FastAPI principal
from database.models import Usuario
from codigos_apoio.security import bcrypt_context
from unittest.mock import Mock

client = TestClient(app) # criação do cliente teste, como um "mini-navegador interno"


# Teste 1, usando um envio válido para login de usuário
def test_login_valido(monkeypatch):
    # cria usuário de teste no banco em memória
    usuario = Usuario(
        nome="Teste1",
        email="email@teste.com",
        senha=bcrypt_context.hash("senha123"),
        ativo=True,
        admin=False
    )

    # Simula o acesso a um banco de dados "falso"
    mock_db = Mock() # usa o mock pra criar ele
    mock_db.query.return_value.filter.return_value.first.return_value = usuario # simula uma validação desse usuario no mock_db

    # Usa monkeypatch do pytest pra aplicar esse mock no endpoint como a base
    from rotas import auth
    # substitui a dependência no app do FastAPI para pular essa necessidade de Session do comportamento completo da função
    app.dependency_overrides[auth.pegar_sessao] = lambda: mock_db

    # Realização da tentativa de login
    resposta = client.post("/auth/login", json={"email": "email@teste.com", "senha": "senha123"}) # post das credenciais corretas para login no client

    assert resposta.status_code == 200 # valida que o status do login é sucesso 
    dados = resposta.json()
    assert "access_token" in dados # valida que houve criação do acess_token
    assert dados["token_type"] == "Bearer" # valida que o token criado é no formato ideal


# Teste 2, usando um envio inválido para login de usuário
def test_login_invalido(monkeypatch):
    usuario = Usuario(
        nome="Teste2",
        email="outro@teste.com",
        senha=bcrypt_context.hash("senha456"),
        ativo=True,
        admin=False
    )

    # Simula o acesso a um banco de dados "falso"
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = usuario # simula uma validação desse usuario no mock_db

    # Usa monkeypatch do pytest pra aplicar esse mock no endpoint como a base
    from rotas import auth
    # substitui a dependência no app do FastAPI para pular essa necessidade de Session do comportamento completo da função
    app.dependency_overrides[auth.pegar_sessao] = lambda: mock_db

    resposta = client.post("/auth/login", json={"email": "outro@teste.com", "senha": "senhaErrada"}) # post das credenciais não correspondentes pra login no client
    assert resposta.status_code == 400 # valida que houve erro ao tentar login errado
    assert resposta.json()["detail"] == "Usuário não encontrado ou credenciais inválidas." # valida o retorno de detalhamento do erro correto


# Teste 3, usando um envio para login de usuário inexistente
def test_login_inexistente(monkeypatch):
    # Simula o acesso a um banco de dados "falso"
    mock_db = Mock()
    mock_db.query.return_value.filter.return_value.first.return_value = None # simula a inexistência desse usuário

    # Usa monkeypatch do pytest pra aplicar esse mock no endpoint como a base
    from rotas import auth
    # substitui a dependência no app do FastAPI para pular essa necessidade de Session do comportamento completo da função
    app.dependency_overrides[auth.pegar_sessao] = lambda: mock_db

    resposta = client.post("/auth/login", json={"email": "outro@teste.com", "senha": "senhaErrada"}) # post de credenciais não cadastradas
    assert resposta.status_code == 400 # valida que houve erro ao tentar login em credenciais inexistentes
    assert resposta.json()["detail"] == "Usuário não encontrado ou credenciais inválidas." # valida o retorno de detalhamento do erro correto