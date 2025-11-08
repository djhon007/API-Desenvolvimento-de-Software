import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app
from rotas import rotinas


client = TestClient(app)


# Define a fixture usada para SIMULAÇÃO DE UM BANCO DE DADOS falso
@pytest.fixture
def mock_db(monkeypatch):
    """Mock da sessão de banco usada pelo endpoint, pra evitar usar o banco original"""
    mock_session = Mock()

    # o add() e commit() precisam existir, mesmo que não façam nada
    mock_session.add = Mock() # Usa o mock para simular as existências
    mock_session.commit = Mock()

    def fake_refresh(obj):
        setattr(obj, "id", 1) # simula a parte de return do id para voltar 1 e não dar erro de tentativa com None pela ausência da função refresh
    mock_session.refresh = Mock(side_effect=fake_refresh) # chama a função como no comportamento normal


    # substitui a dependência get_db no FastAPI
    monkeypatch.setattr("rotas.rotinas.pegar_sessao", lambda: mock_session)
    app.dependency_overrides[rotinas.pegar_sessao] = lambda: mock_session

    return mock_session


# Define a fixture usada para SIMULAÇÃO DE UM USUÁRIO VÁLIDO
@pytest.fixture
def mock_usuario(monkeypatch):
    """Simula a verificação de token para retornar um usuário válido que possa ser usado no teste"""
    from rotas import rotinas
    usuario_falso = Mock() # Usa o mock para simular um usuário no molde
    usuario_falso.id = 1 # dá um id previsível pra ele
    app.dependency_overrides[rotinas.verificar_token] = lambda: usuario_falso # completa a dependência exigida
    return usuario_falso



# Teste 1, fazendo a tentativa de marcar uma rotina concluída de forma válida
def test_marcar_concluida_rotina_valida(mock_db, mock_usuario, monkeypatch):
    # usuário e banco de dados já injetados pelas funções criadas
    # Criação da rotina associada ao usuário
    rotina_falsa = Mock()
    rotina_falsa.id = 1
    rotina_falsa.id_usuario = mock_usuario.id
    rotina_falsa.titulo = "Revisão de Cálculo I"
    rotina_falsa.conteudo = "Derivadas e integrais"
    rotina_falsa.criado_em = "2025-11-08 19:30:00"
    rotina_falsa.concluido = False

    # Associação da rotina com o banco de dados falso
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = rotina_falsa
    mock_db.query.return_value = mock_query

    # Faz a tentativa de concluir já aplicando o id da rotina definido
    response = client.patch("/rotinas/1/concluir")

    # Validações
    assert response.status_code == 200 # valida que foi uma tentativa de sucesso
    body = response.json()

    assert body["id"] == 1 # valida que o id continua 1
    assert body["titulo"] == "Revisão de Cálculo I" # valida que o titulo continua o mesmo
    assert body["conteudo"] == "Derivadas e integrais" # valida que o conteudo também é o mesmo da rotina marcada
    assert body["criado_em"] == "2025-11-08 19:30:00" # valida que a data de criação é a mesma
    assert body["concluido"] == True # valida que houve mudança no status para concluída


# Teste 2, fazendo a tentativa de marcar uma rotina concluída sem ela existir
def test_marcar_concluida_rotina_inexistente(mock_db, mock_usuario, monkeypatch):
    # usuário e banco de dados já injetados pelas funções criadas
    # Sem criação de qualquer rotina

    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None  # Simula não encontrar rotina
    mock_db.query.return_value = mock_query

    # Faz a tentativa de concluir com um id que não é associado a nenhuma rotina
    response = client.patch("/rotinas/2/concluir")

    # Validações
    assert response.status_code == 404 # valida que o status é erro de not found


# Teste 3, fazendo a tentativa de marcar uma rotina que não é associada ao id do usuário como concluída
def test_marcar_concluida_rotina_nao_associada_ao_user(mock_db, mock_usuario, monkeypatch):
    # usuário e banco de dados já injetados pelas funções criadas
    # Criação da rotina sem ser associada ao id do usuário (1)
    rotina_falsa = Mock()
    rotina_falsa.id = 3
    rotina_falsa.id_usuario = 5 # diferente do mock_usuario.id
    rotina_falsa.titulo = "Álgebra Linear"
    rotina_falsa.conteudo = "Geometria Analítica"
    rotina_falsa.criado_em = "2025-11-08 21:15:00"
    rotina_falsa.concluido = False

    # Associação da rotina com o banco de dados falso
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = rotina_falsa
    mock_db.query.return_value = mock_query

    # Faz a tentativa de concluir já aplicando o id da rotina definido
    response = client.patch("/rotinas/3/concluir")

    # Validações
    assert response.status_code == 403 # valida que o status é erro de proibido