from unittest.mock import Mock # uso de Mock pra fazer testes unitários
from codigos_apoio.security import bcrypt_context 
from rotas.auth import autenticar_usuario
from database.models import Usuario


# Teste 1, usando um usuário válido na função de autenticação
def test_autenticar_usuario_valido_mock():
    # cria usuário de teste no banco em memória
    usuario = Usuario(
        nome="Teste1",
        email="email@teste.com",
        senha=bcrypt_context.hash("senha123"),
        ativo=True,
        admin=False
    )

    db_session = Mock()
    # simula caso em que a consulta retorna o usuário normalmente
    db_session.query.return_value.filter.return_value.first.return_value = usuario

    # gera a tentativa de autenticação desse user
    resultado = autenticar_usuario("email@teste.com", "senha123", db_session)

    assert resultado is not False # valida que a autenticação não retornou False, dando certo
    assert hasattr(resultado, "email") # valida que houve email autenticado
    assert resultado.email == "email@teste.com" # valida que o email autenticado foi o mesmo do usuário


# Teste 2, usando um usuário com senha errada nessa função
def test_autenticar_usuario_invalido_senha_mock():
    usuario = Usuario(
        nome="Teste2",
        email="outro@teste.com",
        senha=bcrypt_context.hash("senha456"),
        ativo=True,
        admin=False
    )

    # criação do mock do db_session
    db_session = Mock()
    # simula caso em que a consulta retorna o usuário normalmente
    db_session.query.return_value.filter.return_value.first.return_value = usuario

    # gera a tentativa de autenticação desse usuário com credencial senha conflitante
    resultado = autenticar_usuario("outro@teste.com", "senhaErrada", db_session)

    assert resultado is False # valida que a autenticação retornou False, dando errado


# Teste 3, usando um usuário inexistente nessa função
def test_autenticar_usuario_nao_existe_mock():

    db_session = Mock()
    # simula caso em que a consulta não encontra o usuário
    # db_session.query().filter_by().first.return_value = None
    db_session.query.return_value.filter.return_value.first.return_value = None

    # gera a tentativa de autenticação de um usuário que sequer existe no banco
    resultado = autenticar_usuario("naoexiste@teste.com", "qualquer", db_session)
    assert resultado is False # valida que a autenticação retornou False, dando errado
