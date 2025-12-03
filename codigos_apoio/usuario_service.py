from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import Usuario
from codigos_apoio.schemas import UsuarioSchema
from codigos_apoio.security import bcrypt_context
from codigos_apoio.logs import registrar_acao

def criar_novo_usuario_service(usuario_schema: UsuarioSchema, session: Session) -> Usuario:
    """
    Serviço responsável por criar um novo usuário.
    Engloba validação, segurança (hash), persistência e log.
    """
    # 1. Validação: Verifica se o e-mail já existe
    usuario_existente = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado.")
    
    # 2. Segurança: Criptografa a senha
    senha_criptografada = bcrypt_context.hash(str(usuario_schema.senha))
    
    # 3. Criação do Objeto
    novo_usuario = Usuario(
        usuario_schema.nome,
        usuario_schema.email,
        senha_criptografada,
        usuario_schema.ativo,
        usuario_schema.admin
    )

    # 4. Persistência: Salva no banco
    session.add(novo_usuario)
    session.commit()
    # O refresh carrega o ID gerado e outros campos padrão do banco
    session.refresh(novo_usuario) 

    # 5. Auditoria: Registra o log com o ID correto
    registrar_acao(novo_usuario.id, "/auth/criar_conta", f"Novo usuário criado: {usuario_schema.email}")
    
    return novo_usuario