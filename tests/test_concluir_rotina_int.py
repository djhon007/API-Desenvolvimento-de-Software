import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app
from rotas import rotinas

client = TestClient(app)

# --- FIXTURES ---

@pytest.fixture
def mock_db(monkeypatch):
    """Simula o Banco de Dados"""
    mock_session = Mock()
    mock_session.add = Mock()
    mock_session.commit = Mock()
    
    # Simula o refresh atribuindo um ID caso o objeto não tenha
    def fake_refresh(obj):
        if not hasattr(obj, 'id') or obj.id is None:
            obj.id = 1
    mock_session.refresh = Mock(side_effect=fake_refresh)

    # Substitui a dependência de banco na rota
    app.dependency_overrides[rotinas.pegar_sessao] = lambda: mock_session
    return mock_session

@pytest.fixture
def mock_usuario():
    """Simula um usuário logado"""
    usuario_falso = Mock()
    usuario_falso.id = 1
    # Substitui a dependência de token na rota
    app.dependency_overrides[rotinas.verificar_token] = lambda: usuario_falso
    return usuario_falso

@pytest.fixture
def mock_logger(monkeypatch):
    """Ignora a função de registrar logs para não dar erro no teste"""
    mock_log = Mock()
    monkeypatch.setattr("rotas.rotinas.registrar_acao", mock_log)
    return mock_log


def test_marcar_concluida_rotina_valida(mock_db, mock_usuario, mock_logger):
    #  Dados da rotina que será retornada pelo banco
    rotina_falsa = Mock()
    rotina_falsa.id = 10
    rotina_falsa.id_usuario = mock_usuario.id  # ID 1
    rotina_falsa.titulo = "Estudar Python"
    rotina_falsa.concluido = False
    
    # O Pydantic exige que esses campos sejam strings, não Mocks vazios
    rotina_falsa.conteudo = "Conteúdo detalhado da rotina" 
    rotina_falsa.criado_em = "2025-11-26 12:00:00" 

    # Configuração do Mock
    mock_query = Mock()
    mock_query.filter.return_value = mock_query # Permite .filter().filter()
    mock_query.first.return_value = rotina_falsa # Retorna o objeto preenchido
    mock_db.query.return_value = mock_query

    # Execução
    response = client.patch("/rotinas/10/concluir")

    # Validações
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 10
    assert data["conteudo"] == "Conteúdo detalhado da rotina"

    # Verifica se o commit foi chamado no banco
    mock_db.commit.assert_called_once()

    # CHECK DO OBJETO Garante que a lógica mudou o valor na memória CONCLUIDO = true
    assert rotina_falsa.concluido is True


def test_marcar_concluida_rotina_inexistente(mock_db, mock_usuario, mock_logger):
    #  Configuração do Mock para NÃO achar nada
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None  # Simula banco vazio para esse ID
    
    mock_db.query.return_value = mock_query

    #  Execução com ID inexistente
    response = client.patch("/rotinas/999/concluir")

    #  Validação
    assert response.status_code == 404
    assert response.json()["detail"] == "Rotina não encontrada."


def test_marcar_concluida_rotina_de_outro_usuario(mock_db, mock_usuario, mock_logger):
    #  Dados da rotina de OUTRA pessoa
    rotina_falsa = Mock()
    rotina_falsa.id = 20
    rotina_falsa.id_usuario = 55  # ID diferente do usuário logado (que é 1)
    rotina_falsa.concluido = False

    # Configuração do Mock
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = rotina_falsa # O banco ACHOU a rotina
    
    mock_db.query.return_value = mock_query

    #  Execução
    response = client.patch("/rotinas/20/concluir")

    #  Validação
    assert response.status_code == 403
    assert response.json()["detail"] == "Sem permissão para alterar esta rotina."