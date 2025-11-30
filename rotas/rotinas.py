from fastapi import APIRouter, Depends, HTTPException, status
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from codigos_apoio.dependences import pegar_sessao, verificar_token
from database.models import Rotina, Usuario
from codigos_apoio.schemas import Entrada, Saida, RotinaResponse
from datetime import datetime
from codigos_apoio.dependences import oauth2_schema, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from codigos_apoio.logs import registrar_acao  

load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
rotinas_router = APIRouter(prefix="/rotinas", tags=["rotinas"])


@rotinas_router.post("/gerar-agenda", response_model=RotinaResponse)
def gerar_agenda(req: Entrada, session: Session = Depends(pegar_sessao), usuario=Depends(verificar_token)):
    """Gera um plano de estudo completo com base no Gemini"""
    prompt = f"""
Você é um assistente especializado em organizar planos de estudo de forma lógica, progressiva e realista.

O estudante informou:
- Tema de estudo: "{req.topico_de_estudo}"
- Prazo original: "{req.prazo}"
- Prazo convertido: {req.prazo_em_dias()} dias
...
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json", "response_schema": Saida},
    )

    agenda: Saida = response.parsed
    agenda_texto = "\n".join(agenda.dias_de_estudo)

    nova_rotina = Rotina(
        titulo=req.topico_de_estudo,
        conteudo=agenda_texto,
        criado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        id_usuario=usuario.id
    )

    session.add(nova_rotina)
    session.commit()
    registrar_acao(usuario.id, "/rotinas/gerar-agenda", f"Nova rotina criada: {req.topico_de_estudo}")  
    session.refresh(nova_rotina)
    return nova_rotina


@rotinas_router.get("/listar", response_model=list[RotinaResponse])
async def listar_rotinas_usuario_logado(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(pegar_sessao)
):
    """Lista todas as rotinas criadas pelo usuário autenticado"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # id_usuario = int(payload.get("sub"))
        # if id_usuario is None:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")

        sub_claim = payload.get("sub") # primeiro isola essa captura, porque pode ser none, então não pode tentar converter pra int agora
        if sub_claim is None: # confere se é none
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido.")
        id_usuario = int(sub_claim) # depois, sim, converte pra int

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado.")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

    rotinas = session.query(Rotina).filter(Rotina.id_usuario == usuario.id).all()
    if not rotinas:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma rotina encontrada.")

    registrar_acao(usuario.id, "/rotinas/listar", f"{len(rotinas)} rotinas listadas")  
    return rotinas


@rotinas_router.patch("/{rotina_id}/concluir", response_model=RotinaResponse)
async def marcar_rotina_concluida(
    rotina_id: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """Marca uma rotina como concluída"""
    rotina = session.query(Rotina).filter(Rotina.id == rotina_id).first()
    if not rotina:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rotina não encontrada.")
    if rotina.id_usuario != usuario.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sem permissão.")

    rotina.concluido = True
    session.commit()
    registrar_acao(usuario.id, f"/rotinas/{rotina_id}/concluir", "Rotina marcada como concluída")  
    session.refresh(rotina)
    return rotina
