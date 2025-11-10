from fastapi.testclient import TestClient
from main import app # app FastAPI principal
from database.models import Usuario
from codigos_apoio.security import bcrypt_context
from unittest.mock import Mock

client = TestClient(app) # criação do cliente teste, como um "mini-navegador interno"


# Teste 1, criação de conta válida com credenciais novas
def test_criar_conta_valida(monkeypatch):
    # Simula o acesso a um banco de dados "falso"
    mock_db = Mock() # usa o mock pra criar ele
    mock_db.query.return_value.filter.return_value.first.return_value = None # simula uma não existencia de usuário com mesmo email já cadastrado

    # Usa monkeypatch do pytest pra aplicar esse mock no endpoint como a base
    from rotas import auth
    # substitui a dependência no app do FastAPI para pular essa necessidade de Session do comportamento completo da função
    app.dependency_overrides[auth.pegar_sessao] = lambda: mock_db

    # Realização da tentativa de cadastro de um usuário com credenciais válidas e não já cadastradas
    resposta = client.post("/auth/criar_conta", json={
        "nome": "Teste1",
        "email": "teste1@teste.com",
        "senha": "senha123",
        "ativo": True,
        "admin": False
    }) # post de cadastro válido

    assert resposta.status_code == 200 # valida que o status é de tentativa com sucesso
    
    dados = resposta.json()
    assert dados["mensagem"] == "Usuário cadastrado com sucesso teste1@teste.com."




# Teste 2, tentando criar um usuário já cadastrado no banco
def test_criar_conta_email_repetido(monkeypatch):
    # Criação do usuário base para ser posto no banco mock temporário como já cadastrado
    usuario_existente = Usuario(
        nome="Teste2existente",
        email="teste2@teste.com",
        senha=bcrypt_context.hash("senha123"),
        ativo=True,
        admin=False
    )

    # Simula o acesso a um banco de dados "falso"
    mock_db = Mock() # usa o mock pra criar ele
    mock_db.query.return_value.filter.return_value.first.return_value = usuario_existente # simula uma já existencia do usuário

    # Usa monkeypatch do pytest pra aplicar esse mock no endpoint como a base
    from rotas import auth
    # substitui a dependência no app do FastAPI para pular essa necessidade de Session do comportamento completo da função
    app.dependency_overrides[auth.pegar_sessao] = lambda: mock_db

    # Realização da tentativa de cadastro de um usuário cujo email já está cadastrado
    resposta = client.post("/auth/criar_conta", json={
        "nome": "Teste2novo",
        "email": "teste2@teste.com",
        "senha": "senha456",
        "ativo": True,
        "admin": False
    }) # post de cadastro com credenciais já cadastradas

    assert resposta.status_code == 400 # valida que o status é de erro na tentativa
    assert resposta.json()["detail"] == "E-mail do usuário já cadastrado." # valida o retorno de detalhamento do erro certo