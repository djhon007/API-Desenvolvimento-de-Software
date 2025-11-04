from fastapi import APIRouter, Depends, HTTPException, status
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from codigos_apoio.dependences import pegar_sessao
from database.models import Rotina, Usuario
from codigos_apoio.dependences import pegar_sessao, verificar_token
from codigos_apoio.schemas import Entrada, Saida, RotinaResponse
from datetime import datetime
from codigos_apoio.dependences import oauth2_schema, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

#carrega variáveis do arquivo .env (para acessar GENAI_API_KEY, por exemplo)
load_dotenv()

#inicializa o cliente da api do gemini, usando a chave do .env
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

#cria o roteador fastapi (prefixo para as rotas dessa parte da aplicação)
rotinas_router = APIRouter(prefix="/rotinas", tags=["rotinas"])


@rotinas_router.post("/gerar-agenda", response_model=RotinaResponse)
def gerar_agenda(req: Entrada, session: Session = Depends(pegar_sessao), usuario= Depends(verificar_token)):
    """
    Gera o plano de estudos pelo Gemini
    """

    #monta o prompt (texto enviado ao modelo Gemini)
    prompt = f"""
Você é um assistente especializado em organizar planos de estudo de forma lógica, progressiva e realista.

O estudante informou:
- Tema de estudo: "{req.topico_de_estudo}"
- Prazo original: "{req.prazo}"
- Prazo convertido: {req.prazo_em_dias()} dias

Crie um **plano de estudos completo**, dividido em exatamente {req.prazo_em_dias()} dias, numerados de 1 até {req.prazo_em_dias()}.

Cada item deve seguir o formato:
"Dia X: [conteúdo a ser estudado]"

Regras importantes:
- Crie exatamente {req.prazo_em_dias()} itens (nem mais, nem menos).
- Use linguagem clara e objetiva.
- Estruture o plano de forma progressiva — comece com os conceitos básicos e avance para os mais complexos.
- Se o prazo for maior que o necessário, utilize os dias restantes com revisões, exercícios ou aplicações práticas.
- NÃO inclua explicações fora do formato JSON.

Formato esperado (exemplo para 3 dias):
{{
  "dias_de_estudo": [
    "Dia 1: Introdução ao tema e conceitos básicos",
    "Dia 2: Estudo aprofundado dos principais tópicos",
    "Dia 3: Revisão geral e exercícios práticos"
  ]
}}

Retorne **somente o JSON**, nada mais.
"""

    #chama o modelo gemini com o prompt e define que a resposta deve vir em formato JSON
    response = client.models.generate_content(
        model="gemini-2.5-flash",               
        contents=prompt,                        
        config={                                
            "response_mime_type": "application/json",  
            "response_schema": Saida,                  
        },
    )

    #converte a resposta json em um objeto da classe saida do schematics
    agenda: Saida = response.parsed

    #junta todas as linhas do plano de estudo em um único texto
    agenda_texto = "\n".join(agenda.dias_de_estudo)

    #cria uma nova instância da tabela Rotina (objeto ORM do SQLAlchemy)
    nova_rotina = Rotina(
        #título vem do topico
        titulo=req.topico_de_estudo, 
        #conteúdo gerado pelo gemini                   
        conteudo=agenda_texto,   
        #data/hora atual formatada                       
        criado_em=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        #usuário dono da rotina
        id_usuario=usuario.id                        
    )

    #adiciona a nova rotina ao banco de dados
    session.add(nova_rotina)

    #confirma a inserção (salva no banco)
    session.commit()

    #atualiza o objeto `nova_rotina` com os dados do banco
    session.refresh(nova_rotina)

    #retorna a rotina recém-criada (como resposta da API)
    return nova_rotina

#listar todas rotinas do usuario

@rotinas_router.get("/listar", response_model=list[RotinaResponse])
async def listar_rotinas_usuario_logado(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(pegar_sessao)
):
    """
    Lista todas as rotinas criadas pelo usuário autenticado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(payload.get("sub"))  # usa o ID do token
        if id_usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: ID do usuário não encontrado.",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
        )

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    rotinas = session.query(Rotina).filter(Rotina.id_usuario == usuario.id).all()

    if not rotinas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhuma rotina encontrada para este usuário.",
        )

    return rotinas
