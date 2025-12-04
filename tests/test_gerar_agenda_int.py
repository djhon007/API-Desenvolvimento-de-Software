import pytest
from unittest.mock import Mock
from fastapi.testclient import TestClient
from main import app
from codigos_apoio.dependences import pegar_sessao
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


# Teste 1, criação de uma agenda válida
def test_criar_agenda_sucesso(mock_db, mock_usuario, monkeypatch):
    """
    Testa a geração de agenda com sucesso, mockando a resposta da IA.
    """
    # 0. TRAVA DE SEGURANÇA: Garantimos que a API use O NOSSO mock_db
    # Isso resolve o problema de instâncias trocadas
    app.dependency_overrides[pegar_sessao] = lambda: mock_db

    # 1. Mock da resposta do Google Gemini
    mock_saida = Mock()
    mock_saida.parsed = Mock() 
    mock_saida.parsed.dias_de_estudo = [
        "Dia 1: Revisão de derivadas",
        "Dia 2: Integrais",
        "Dia 3: Aplicações"
    ]
    
    mock_client = Mock()
    mock_client.models.generate_content.return_value = mock_saida
    
    monkeypatch.setattr("rotas.rotinas.get_google_client", lambda: mock_client)

    # 2. Configura o comportamento do Banco (Simular Auto-Incremento)
    # Quando 'session.add' for chamado, injetamos o ID 1 na hora
    def simulate_add(instance):
        instance.id = 1 
    
    mock_db.add.side_effect = simulate_add

    # 3. Payload
    payload = {
        "topico_de_estudo": "Cálculo 1",
        "prazo": "3 dias"
    }

    # 4. Execução
    response = client.post("/rotinas/gerar-agenda", json=payload)

    # 5. Validação
    assert response.status_code == 200
    data = response.json()
    
    # Agora o ID deve vir preenchido, pois configuramos o mock certo!
    assert data["id"] == 1
    assert data["titulo"] == "Cálculo 1"
    assert "Revisão de derivadas" in data["conteudo"]
