from fastapi.testclient import TestClient
from main import app # app FastAPI principal
from unittest.mock import Mock
from rotas.auth import criar_token # função base para o refresh

client = TestClient(app) # criação do cliente teste, como um "mini-navegador interno"


# Teste 1, refresh básico
def test_refresh_token_valido(monkeypatch):
    from rotas import auth

    # simula um usuário "logado"
    usuario_falso = Mock()
    usuario_falso.id = 1 # id básico aplicado ao usuário

    # sobrescreve a dependência que o FastAPI usa internamente em verificar_token pra isolar o comportamento da função
    app.dependency_overrides[auth.verificar_token] = lambda: usuario_falso

    # sobrescreve criar_token pra gerar algo previsível
    monkeypatch.setattr(auth, "criar_token", lambda user_id: f"fake_token_{user_id}")

    # faz a chamada ao endpoint /auth/refresh
    resposta = client.post("/auth/refresh")

    # validações
    assert resposta.status_code == 200 # validação que deu certo, com status 200

    dados = resposta.json()
    assert "access_token" in dados # validação que há token de acesso
    assert dados["access_token"] == "fake_token_1" # validação de que o token é correspondente
    assert dados["token_type"] == "Bearer" # validação do seu tipo