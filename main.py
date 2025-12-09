
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from rotas.auth import auth_router
from rotas.rotinas import rotinas_router
from dotenv import load_dotenv
import os 
from fastapi.security import OAuth2PasswordBearer
from codigos_apoio.erros import tratar_excecoes



#inicializando o fastapi
app = FastAPI()


#LIBERANDO O FRONT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return Response(status_code=200)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
#registrando as rotas
app.include_router(auth_router)
app.include_router(rotinas_router)

app.add_exception_handler(Exception, tratar_excecoes)