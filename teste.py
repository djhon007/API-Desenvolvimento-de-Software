from google import genai
import os

client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

# Inicializa o chat com instruções fixas
chat = client.chats.create(
    model="gemini-2.5-flash-lite",
    history=[
        {
            "role": "user",
            "parts": [{"text": "Você é um assistente especializado em gestão de tempo. "
                               "Ajude a organizar horários de estudo, trabalho e lazer. "
                               "Não fale sobre outros assuntos. "
                               "Ao iniciar, cumprimente o usuário e explique como você pode ajudar."}]
        }
    ]
)

# Mensagem inicial automática
welcome = chat.send_message("Inicie a conversa com a mensagem de boas-vindas. Sou uma IA especializada em gestão de tempo!")
print("AI:", welcome.text)

while True:
    message = input("You: ")
    if message == "exit":
        break
    response = chat.send_message(message)
    print("AI:", response.text)
