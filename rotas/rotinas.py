from fastapi import APIRouter, Depends, HTTPException, status
from google import genai
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from datetime import datetime
from jose import jwt, JWTError

from codigos_apoio.dependences import (
    pegar_sessao,
    verificar_token,
    oauth2_schema,
    SECRET_KEY,
    ALGORITHM
)

from database.models import Rotina, Usuario
from codigos_apoio.schemas import Entrada, Saida, RotinaResponse, RotinaCreate
from codigos_apoio.logs import registrar_acao

# =========================
# CONFIGURAÇÕES
# =========================
load_dotenv()
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

rotinas_router = APIRouter(
    prefix="/rotinas",
    tags=["rotinas"]
)

# =========================
# GERAR AGENDA
# =========================


@rotinas_router.post("/gerar-agenda")
def gerar_agenda(
    req: Entrada,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    tipo = req.tipo_planejamento()
    quantidade = req.prazo_numero()

    topicos = req.topico_de_estudo.replace("|", ",")

    prompt = f"""
Você é um assistente especializado em criar planos de estudo claros, realistas e bem organizados.

O estudante informou:
- Tópico(s) de estudo: "{topicos}"
- Prazo: "{req.prazo}"

REGRAS OBRIGATÓRIAS:

 Se o prazo for em DIAS:
- Organize como:
  Dia 1: ...
  Dia 2: ...

 Se o prazo for em HORAS:
- Organize como:
  Hora 1: ...
  Hora 2: ...

 Se o prazo for em MINUTOS:
- Gere APENAS uma tarefa objetiva.
- NÃO divida em etapas.

 Se houver MAIS DE UM tópico:
- Divida o tempo de forma equilibrada.
- Indique claramente qual tópico está sendo estudado em cada etapa.

 Retorne APENAS no formato JSON abaixo:
{{
  "dias_de_estudo": ["..."]
}}

Tipo de planejamento: {tipo}
Quantidade de unidades: {quantidade}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": Saida
        }
    )

    agenda: Saida = response.parsed
    agenda_texto = "\n".join(agenda.dias_de_estudo)

    registrar_acao(
        usuario.id,
        "/rotinas/gerar-agenda",
        f"Agenda gerada ({tipo})"
    )

    return {
        "titulo": req.topico_de_estudo,
        "conteudo": agenda_texto
    }


@rotinas_router.get("/listar", response_model=list[RotinaResponse])
async def listar_rotinas_usuario_logado(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(pegar_sessao)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))
        if id_usuario is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Token inválido ou expirado.")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    rotinas = session.query(Rotina).filter(
        Rotina.id_usuario == usuario.id).all()
    if not rotinas:
        raise HTTPException(
            status_code=404, detail="Nenhuma rotina encontrada.")

    registrar_acao(usuario.id, "/rotinas/listar",
                   f"{len(rotinas)} rotinas listadas")
    return rotinas


@rotinas_router.patch("/{rotina_id}/concluir", response_model=RotinaResponse)
async def marcar_rotina_concluida(
    rotina_id: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    rotina = session.query(Rotina).filter(Rotina.id == rotina_id).first()
    if not rotina:
        raise HTTPException(status_code=404, detail="Rotina não encontrada.")

    if rotina.id_usuario != usuario.id:
        raise HTTPException(status_code=403, detail="Sem permissão.")

    rotina.concluido = True
    session.commit()
    session.refresh(rotina)

    registrar_acao(
        usuario.id,
        f"/rotinas/{rotina_id}/concluir",
        "Rotina marcada como concluída"
    )

    return rotina


@rotinas_router.post("/salvar", response_model=RotinaResponse)
def salvar_roteiro(
    roteiro: RotinaCreate,
    usuario: Usuario = Depends(verificar_token),
    session: Session = Depends(pegar_sessao)
):
    nova_rotina = Rotina(
        titulo=roteiro.titulo,
        conteudo=roteiro.conteudo,
        criado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        id_usuario=usuario.id
    )

    session.add(nova_rotina)
    session.commit()
    session.refresh(nova_rotina)

    return nova_rotina


@rotinas_router.delete("/{rotina_id}/excluir", response_model=RotinaResponse)
def excluir_rotina(
    rotina_id: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    rotina = session.query(Rotina).filter(Rotina.id == rotina_id).first()

    if not rotina:
        raise HTTPException(status_code=404, detail="Rotina não encontrada.")

    if rotina.id_usuario != usuario.id:
        raise HTTPException(
            status_code=403, detail="Sem permissão para excluir esta rotina.")

    session.delete(rotina)
    session.commit()

    return rotina
