import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app

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


# Teste 1, criação de uma agenda válida
def test_criar_agenda_sucesso(mock_db, mock_usuario, monkeypatch):
    from rotas import rotinas

    # Usa o mock para simular a resposta do Gemini
    mock_saida = Mock()
    mock_saida.parsed = Mock()
    mock_saida.parsed.dias_de_estudo = [
        "Dia 1: Revisão de derivadas",
        "Dia 2: Integrais",
        "Dia 3: Aplicações"
    ]

    monkeypatch.setattr(rotinas.client.models, "generate_content", lambda **kwargs: mock_saida) # simula a parte de generate_content com a predefinição mock_saida para evitar chamada da gemini no test

    # Montagem da entrada simulada de acodo com os requisitos para a geração
    dados_envio = {
        "topico_de_estudo": "Cálculo II",
        "prazo": "3 dias"
    }

    monkeypatch.setattr("rotas.rotinas.Rotina.id", 1)

    response = client.post("/rotinas/gerar-agenda", json=dados_envio) # simula um post para gerar agenda com os dados de envio definidos

    assert response.status_code == 200  # valida que foi criado com sucesso
    body = response.json()

    assert "id" in body # valida que há um id entre os dados
    assert body["titulo"] == "Cálculo II" # valida que o título corresponde ao pedido
    assert len(body["conteudo"].split("\n")) == 3 # valida que o conteúdo junta todas as divisões de dias de estudo
    assert "criado_em" in body # valida que a informação de data de criação também é retornada 
    assert "conteudo" in body  # pra garantir que o texto gerado a partir da divisão de conteúdos está presente
