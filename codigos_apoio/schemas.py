from pydantic import BaseModel
from typing import Optional
from typing import List

#define o formato de dados esperados pela API
class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


from pydantic import BaseModel
from typing import List
import re

class Entrada(BaseModel):
    topico_de_estudo: str
    prazo: str

    #metodos para entrada
    def prazo_numero(self):
        match = re.search(r"\d+", self.prazo)
        return int(match.group()) if match else 0

    def prazo_palavra(self):
        match = re.search(r"[A-Za-zÀ-ÿ]+", self.prazo)
        return match.group().lower() if match else "dias"

    def prazo_em_dias(self):
        palavra = self.prazo_palavra()
        numero = self.prazo_numero()

        if palavra in ["semana", "semanas"]:
            return numero * 7
        elif palavra in ["mes", "mês", "meses"]:
            return numero * 30
        else:
            return numero


class Saida(BaseModel):
    dias_de_estudo: List[str]


class RotinaResponse(BaseModel):
    id :int
    titulo: str
    conteudo: str
    criado_em: str

    class Config:
        from_attributes = True

#login
class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True


class RotinaCreate(BaseModel):
    titulo: str
    conteudo: str
