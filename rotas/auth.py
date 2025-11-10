from fastapi import APIRouter, Depends, HTTPException
from database.models import Usuario, db
from codigos_apoio.dependences import pegar_sessao, verificar_token
from codigos_apoio.security import bcrypt_context
from codigos_apoio.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from codigos_apoio.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
from codigos_apoio.logs import registrar_acao  

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.get('/')
async def home():
    """Rota padrão de autentificação"""
    return {"mensagem": "Você acessou a rota padrão de autentificação", "autentificando": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado.")
    
    senha_criptografada = bcrypt_context.hash(str(usuario_schema.senha))
    novo_usuario = Usuario(
        usuario_schema.nome,
        usuario_schema.email,
        senha_criptografada,
        usuario_schema.ativo,
        usuario_schema.admin
    )

    session.add(novo_usuario)
    session.commit()

    registrar_acao(0, "/auth/criar_conta", f"Novo usuário: {usuario_schema.email}")  
    return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}."}


def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario or not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    if not usuario.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo.")

    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

    registrar_acao(usuario.id, "/auth/login", "Login realizado com sucesso") 
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "Bearer"}


@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")

    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

    registrar_acao(usuario.id, "/auth/login-form", "Login via formulário realizado")  
    return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.post("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    registrar_acao(usuario.id, "/auth/refresh", "Token renovado com sucesso")  
    return {"access_token": access_token, "token_type": "Bearer"}
