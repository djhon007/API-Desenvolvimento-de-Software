from google import genai
from pydantic import BaseModel
import os
from fastapi import FastAPI

#inciializado o fastapi
app = FastAPI()

#incializando o cliente gemini
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))


#modelos de entrada e de saída
class Entrada(BaseModel):
    topico_de_estudo: str
    prazo: str

    #Função que extrai o número (quantidade) do campo "prazo"
    @property
    def prazo_numero(self):
        import re  # Importa o módulo de expressões regulares (regex), usado para buscar padrões em texto

        # Procura na string 'self.prazo' uma sequência de um ou mais dígitos (0–9)
        match = re.search(r"\d+", self.prazo) # Procura na string 'self.prazo' uma sequência de um ou mais dígitos (0–9)

        # Se encontrou um número, converte para inteiro e retorna
        # Caso contrário (ex: se o usuário digitou algo sem número), retorna 0 por padrão
        return int(match.group()) if match else 0
    # 🔹 Propriedade que extrai a unidade de tempo (palavra) do campo "prazo"
    @property
    def prazo_palavra(self):
        import re  # Importa novamente o módulo de expressões regulares

        # Procura na string 'self.prazo' uma sequência de letras (A-Z ou com acento)
        match = re.search(r"[A-Za-zÀ-ÿ]+", self.prazo)

        # Se encontrou uma palavra, transforma em minúsculas e retorna, se nao encontrou, retorna "dias" como valor padrão
        return match.group().lower() if match else "dias"
    
    #padronizando prazos para dias
    def prazo_em_dias(self):
        if self.prazo_palavra == "semanas" or self.prazo_palavra == "semana":
           return self.prazo_numero *7
        elif self.prazo_palavra == "meses" or self.prazo_palavra == "mes" or self.prazo_palavra == "mês":
            return self.prazo_numero * 30
        else:
            return self.prazo_numero



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
    #prompt que eu criei
    contents= prompt, 
    config={
        "response_mime_type": "application/json",
        "response_schema": list[Saída], #ensina ao gemini a transformar esse JSON em uma lista de objetos python do tipo rotina
    },
    )

    #converte a resposta da API em uma lista de objetos Rotina para facilitar o acesso aos dados.
    agenda: list[Saída] = response.parsed

    # retorna a resposta final para o front-end em formato JSON
    # cada item em 'agenda' é um objeto Pydantic do tipo 'Saída'
    # o método .dict() converte esses objetos em dicionários Python
    # a list comprehension [a.dict() for a in agenda] cria uma lista com esses dicionários
    # por fim, tudo é agrupado dentro de um dicionário com a chave "agenda"
    # o FastAPI converte automaticamente esse dicionário em JSON antes de enviar ao front-end
    return {"agenda": [a.dict() for a in agenda]}
    

    #para testar: 
    #1- inicializar a chave da api: export GENAI_API_KEY="sua_chave_aqui"
    #2- colocar isso no terminal: uvicorn main:app --reload
    #3- abrir esse link: http://127.0.0.1:8000/docs

