from datetime import timedelta, datetime, timezone # como vai usar análise de tempo, importa isso
from jose import jwt # para validação do token
from codigos_apoio.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES # para usar na função jwt
from rotas.auth import criar_token # função testada



# Teste 1, para geração de um token con tempo padrão
def test_criar_token_padrao_unit():
    # gera um token com o tempo padrão
    token = criar_token(123)  # id fictício de usuário
    decodificado = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # faz a decodificação pra verificar o token

    # verifica se contém o identificador do usuário "sub" igual ao id
    assert decodificado["sub"] == "123" 

    # verifica se contém a chave de expiração necessária para a geração de token
    assert "exp" in decodificado



# Teste 2, para geração de um token con tempo customizado
def test_criar_token_duracao_custom_unit():
    # gera um token com tempo personalizado
    duracao = timedelta(minutes=1)
    inicio = datetime.now(timezone.utc)
    token = criar_token(456, duracao_token=duracao) # id fictício de usuário e duração especificada
    decodificado = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # faz a decodificação pra verificar o token

    exp = datetime.fromtimestamp(decodificado["exp"], tz=timezone.utc)
    diferenca = exp - inicio

    # tolerância de até 10 segundos pra diferenças de tempo e visão geral da duração esperada na especificação
    assert abs(diferenca.total_seconds() - 60) < 10