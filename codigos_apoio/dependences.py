from fastapi import Depends, HTTPException, status
from codigos_apoio.config import SECRET_KEY, ALGORITHM
from database.models import db
from sqlalchemy.orm import sessionmaker, Session
from database.models import Usuario
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")


def pegar_sessao():
    try:
        #abrindo sessao no banco de dados
        Session = sessionmaker(bind=db)
        session = Session()
        #retorna sessao e dps fecha
        yield session
    finally:
        #sempre vai entrar aq
        #fecha a sessao
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))

        if id_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: ID do usuário ausente."
            )

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso Negado, verifique a válidade do token")
    
    # Busca o usuário correspondente no banco de dados
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Acesso Inválido.")
    return usuario