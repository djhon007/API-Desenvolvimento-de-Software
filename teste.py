from google import genai
from pydantic import BaseModel
import os


#parte que eu adaptei
topico_de_estudo = input("Qual é o tópico de estudo que você quer estudar?")
prazo = input("Quantos dias você tem?")
#parte que o site aistudio traz
class Rotina(BaseModel):

   dias_de_estudo: list[str]
   horarios:list[str]

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))
response = client.models.generate_content(
   model="gemini-2.5-flash",
   #prompt que eu criei
   contents=(f"Você é um assistente virtual especializado em ajudar estudantes, principalmente universitários, a organizarem seus estudos de forma clara, lógica e eficiente. Seu objetivo é reduzir a ansiedade e aumentar o foco dos alunos, oferecendo um plano de estudos personalizado, específico e detalhado.O estudante fornecerá um tema de estudo (representado como {topico_de_estudo}) e o número de dias restantes até a prova (representado como {prazo}). A partir disso, sua tarefa é dividir o tema em subtópicos organizados de forma hierárquica, respeitando a ordem lógica de aprendizado — começando pelos conceitos mais básicos e evoluindo gradualmente para os mais complexos.Distribua esses subtópicos de forma equilibrada ao longo dos {prazo} dias disponíveis. Seja específico ao indicar o que deve ser estudado a cada dia. Evite sugestões vagas como 'revisar conteúdo' ou 'estudar um pouco'. Use linguagem objetiva e clara, formatada como uma lista.A resposta deve estar exclusivamente no formato JSON que segue a estrutura da classe Rotina, especificamente no campo dias_de_estudo, contendo exatamente {prazo} itens. Cada item da lista deve seguir o modelo: 'Dia X: [conteúdo a ser estudado]', substituindo X pelo número do dia, e o conteúdo deve ser coerente com a progressão dos estudos.Se o tema for muito amplo, divida-o proporcionalmente ao tempo disponível. Se for curto, utilize o tempo restante com revisões inteligentes, exercícios ou práticas, mas preencha todos os dias com atividades úteis. Não inclua nenhuma explicação fora da estrutura JSON especificada."),
   config={
       "response_mime_type": "application/json",
       "response_schema": list[Rotina], #ensina ao gemini a transformar esse JSON em uma lista de objetos python do tipo rotina
   },
)

#converte a resposta da API em uma lista de objetos Rotina para facilitar o acesso aos dados.
agenda: list[Rotina] = response.parsed

#imprimindo de forma organizada (parte que eu adaptei o print)
def imprimir_agenda(agenda):


   for dia in agenda:
       print("Seu Roteiro de Estudos:")
       print()
       print()
       for dia_de_estudo in dia.dias_de_estudo:
           print(f"  - {dia_de_estudo}")
           print()


imprimir = imprimir_agenda(agenda)
#print(agenda)
