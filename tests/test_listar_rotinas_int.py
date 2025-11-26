import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app
from rotas import rotinas
from codigos_apoio.schemas import RotinaResponse

client = TestClient(app)


# Define a fixture usada para SIMULAÇÃO DE UM BANCO DE DADOS falso
@pytest.fixture
def mock_db(monkeypatch):
    """Mock da sessão de banco"""
    mock_session = Mock()
    mock_session.add = Mock()
    mock_session.commit = Mock()
    
    # Substitui a dependência get_db no FastAPI
    app.dependency_overrides[rotinas.pegar_sessao] = lambda: mock_session
    return mock_session


# Define a fixture do token necessário para identificação do usuário e listagem de rotinas específicas
@pytest.fixture
def mock_token(monkeypatch):
    """Simula decodificação JWT com ID de usuário válido (1)"""
    monkeypatch.setattr("jose.jwt.decode", lambda *a, **kw: {"sub": "1"})
    return "fake_token"

# Define a fixture de log
@pytest.fixture
def mock_logger(monkeypatch):
    """Evita erro de log durante o teste"""
    mock_log = Mock()
    monkeypatch.setattr("rotas.rotinas.registrar_acao", mock_log)
    return mock_log


# Teste 1, listagem de rotinas existentes de um usuário válido
def test_listar_rotinas_sucesso(mock_db, mock_token, monkeypatch):
    # Mock do usuário
    usuario_falso = Mock() # usa mock pra cobrir a existência de um usuário com molde
    usuario_falso.id = 1 # dá o id previsível

    # rotina falsa
    rotina_falsa = Mock()
    rotina_falsa.id = 1
    rotina_falsa.titulo = "Cálculo II"
    rotina_falsa.conteudo = "Dia 1: Revisão de derivadas"
    rotina_falsa.criado_em = "2025-11-05 10:00:00"
    rotina_falsa.id_usuario = 1
    rotina_falsa.concluido = False

    mock_query = Mock()
    mock_query.filter.return_value = mock_query

    mock_query.first.return_value = usuario_falso # buscando o usuario
    mock_query.all.return_value = [rotina_falsa] # buscando a rotina

    mock_db.query.return_value = mock_query # conecta ao banco

    # faz a tentativa de listar as rotinas desse usuário
    response = client.get("/rotinas/listar", headers={"Authorization": f"Bearer {mock_token}"})

    assert response.status_code == 200 # valida que foi uma tentativa com sucesso
    body = response.json()

    # deve retornar uma lista com pelo menos 1 rotina
    assert isinstance(body, list) # valida que está no formato esperado da lista
    assert len(body) > 0 # valida que não retornou lista vazia

    rotina = body[0] # pega uma rotina e vê se seu comportamento está correto
    assert rotina["id"] == 1 # valida o id da rotina
    assert rotina["titulo"] == "Cálculo II" # valida o título da rotina
    assert "conteudo" in rotina # valida que há conteudo
    assert len(rotina["conteudo"].split("\n")) == 1 # valida que o conteúdo está dividido conforme o comportamento esperado e dados de resposta
    assert "criado_em" in rotina # valida que há data de criação