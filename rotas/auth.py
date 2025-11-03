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

#cria o roteador do FastAPI com prefixo '/auth'
#todas as rotas desse arquivo estarão sob /auth (ex: /auth/login)
auth_router = APIRouter(prefix='/auth', tags=['auth'])


#rota inicial de autenticação — apenas retorna uma mensagem simples
@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autentificação do nosso sistema
    """
    return {"mensagem": "Você acessou a rota padrão de autentificação", "autentificando": False}


#endpoint para criar uma conta (registro de novo usuário)
@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    #verifica se já existe um usuário com o mesmo e-mail
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario:
        #se já existir, gera erro 400 (Bad Request)
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado.")
    else:
        #criptografa a senha do usuário usando o bcrypt_context
        senha_criptografada = bcrypt_context.hash(str(usuario_schema.senha))

        #cria uma instância de usuário com os dados enviados
        novo_usuario = Usuario(
            usuario_schema.nome,
            usuario_schema.email,
            senha_criptografada,
            usuario_schema.ativo,
            usuario_schema.admin
        )

        #adiciona o novo usuário à sessão e salva no banco
        session.add(novo_usuario)
        session.commit()

        #retorna mensagem de sucesso
        return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}."}


#função para gerar tokens JWT
def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    #define o tempo de expiração com base no tempo atual + duração configurada
    data_expiracao = datetime.now(timezone.utc) + duracao_token

    #cria o payload (informações codificadas dentro do token)
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}

    #codifica o token usando a SECRET_KEY e o algoritmo definido (HS256)
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    #retorna o token JWT final
    return jwt_codificado


#função auxiliar para autenticar o usuário (verifica e-mail e senha)
def autenticar_usuario(email, senha, session):
    #busca o usuário pelo e-mail
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        #usuário não encontrado
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        #senha incorreta
        return False

    #se passou pelas verificações, retorna o objeto do usuário
    return usuario


#endpoint de login, gera tokens (access e refresh)
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    #verifica credenciais usando a função auxiliar
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        #se o usuário não existir ou senha errada, erro 400
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    else:
        #cria o access token (curta duração)
        access_token = criar_token(usuario.id)

        #cria o refresh token (duração de 7 dias)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

        #retorna os tokens ao cliente
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    #verifica credenciais usando a função auxiliar
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)

    if not usuario:
        #se o usuário não existir ou senha errada, erro 400
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    else:
        #cria o access token (curta duração)
        access_token = criar_token(usuario.id)

        #cria o refresh token (duração de 7 dias)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

        #retorna os tokens ao cliente
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }





#endpoint para gerar novo access_token usando o refresh_token
@auth_router.post("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    #cria novo access_token
    access_token = criar_token(usuario.id)
    #retorna o novo token
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
