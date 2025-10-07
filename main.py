from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# carrega o arquivo .env logo no início
load_dotenv()

# inciializado o fastapi
app = FastAPI()

# LIBERANDO O FRONT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# incializando o cliente gemini
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))


# modelos de entrada e de saída
class Entrada(BaseModel):
    topico_de_estudo: str
    prazo: str

    #organizando prazo(numero)
    def prazo_numero(self):
        import re
        #procura na string uma sequencia de um ou mais digitos de 0 - 9
        match = re.search(r"\d+", self.prazo)
        #se achou, retorna o numero em formarto de int, caso contrario, retorna 0
        return int(match.group()) if match else 0

    #organizando prazo(palavras)
    def prazo_palavra(self):
        import re
        #procura letras maiusculas e minusculas, com acento ou sem
        match = re.search(r"[A-Za-zÀ-ÿ]+", self.prazo)
        #se achou, retorna a palavra, caso contrario retorna "dias"
        return match.group().lower() if match else "dias"

    #padroniza a unidade de medida para dias
    def prazo_em_dias(self):
        palavra = self.prazo_palavra()  
        numero = self.prazo_numero()    

        if palavra in ["semana", "semanas"]:
            return numero * 7
        elif palavra in ["mes", "mês", "meses"]:
            return numero * 30
        else:
            return numero


class Saída(BaseModel):
    dias_de_estudo: list[str]


@app.post("/gerar-agenda")
def gerar_agenda(req: Entrada):
    """
    Gera o plano de estudos pelo Gemini
    """

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        # prompt que eu criei
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            # ensina ao gemini a transformar esse JSON em uma lista de objetos python do tipo rotina
            "response_schema": list[Saída],
        },
    )

    # converte a resposta da API em uma lista de objetos Rotina para facilitar o acesso aos dados.
    agenda: list[Saída] = response.parsed

    # retorna a resposta final para o front-end em formato JSON
    # cada item em agenda é um objeto Pydantic do tipo Saída, o.dict() converte os objetos em dicionairo, e o metodo list (a.dict() for a ...) cria uma lista com os dicionarios
    #tudo é agrupado dentro de um dicionário com a chave agenda
    return {"agenda": [a.dict() for a in agenda]}

    
    
    # para criar ambiente virtual
    # 1- python3 -m venv venv
    # 2-source venv/bin/activate

    #bibliotecas: pip install fastapi uvicorn google-genai python-dotenv pydantic

    # para testar:
    # 1- criar arquivo .env, e digitar exatamente isso: GENAI_API_KEY="sua_chave_aqui"
    # 2- colocar isso no terminal: uvicorn main:app --reload (verificar se o terminal esta rodando dentro do caminho certo para a pasta que está o main.py)
    # 3- inicalizar o front: criar um novo terminal, e colocar isso nele(verificar se o terminal está na pasta "frontend"): python3 -m http.server 8080
    # 4- depois que inicializou o front: abrir esse link: http://127.0.0.1:8080

