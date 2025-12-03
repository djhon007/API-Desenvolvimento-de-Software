from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta 

# Importações do Projeto
from database.models import Usuario
from codigos_apoio.dependences import pegar_sessao, verificar_token
from codigos_apoio.schemas import UsuarioSchema, LoginSchema
from codigos_apoio.logs import registrar_acao

# --- CORREÇÃO: Adicionado o import que faltava ---
from codigos_apoio.usuario_service import criar_novo_usuario_service
# -------------------------------------------------

# Importamos as funções de segurança (Refatoração 3)
from codigos_apoio.security import criar_token, autenticar_usuario, bcrypt_context
# -------------------------------------------------------------

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.get('/')
async def home():
    """Rota padrão de autentificação"""
    return {"mensagem": "Você acessou a rota padrão de autentificação", "autentificando": False}


# --- FUNÇÃO REFATORADA ---
@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """
    Rota para criação de conta. 
    Agora atua apenas como Controlador, delegando a lógica para o Service.
    """
    usuario_criado = criar_novo_usuario_service(usuario_schema, session)
    
    return {"mensagem": f"Usuário cadastrado com sucesso {usuario_criado.email}."}


def _processar_autenticacao(usuario: Usuario, endpoint_path: str):
    """
    Processa a lógica de criação de tokens e logs após a autenticação bem-sucedida.
    Garante a verificação de usuário ativo de forma consistente.
    """
    if not usuario.ativo:
        raise HTTPException(status_code=400, detail="Usuário inativo.")

    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

    registrar_acao(usuario.id, endpoint_path, "Login processado com sucesso")
    
    return {"access_token": access_token, "refresh_token": refresh_token}


# ROTA /login REFATORADA
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")
    
    # Chama a nova função para processar o login (sem duplicação de lógica)
    tokens = _processar_autenticacao(usuario, "/auth/login")

    # Retorna o resultado completo esperado por esta rota (access_token + refresh_token)
    return {"access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"], "token_type": "Bearer"}


# ROTA /login-form REFATORADA
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)): # pragma: no cover
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas.")

    # Chama a nova função (garante a checagem de 'ativo' e o log)
    tokens = _processar_autenticacao(usuario, "/auth/login-form")

    # Retorna APENAS o access_token, conforme o comportamento original desta rota
    return {"access_token": tokens["access_token"], "token_type": "Bearer"}


@auth_router.post("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    registrar_acao(usuario.id, "/auth/refresh", "Token renovado com sucesso")  
    return {"access_token": access_token, "token_type": "Bearer"}
