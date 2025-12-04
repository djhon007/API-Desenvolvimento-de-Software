from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database.models import Usuario
from codigos_apoio.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# Contexto de Criptografia (Hash de senha)
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_token(id_usuario: int, duracao_token: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Gera um token JWT para um usuário.
    Se nenhuma duração for passada, usa o padrão do arquivo .env/config.
    """
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": str(id_usuario),
        "exp": data_expiracao
    }
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email: str, senha: str, session: Session):
    """
    Busca usuário pelo email e verifica se a senha bate com o hash.
    Retorna o objeto Usuario ou False.
    """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
        
    return usuario