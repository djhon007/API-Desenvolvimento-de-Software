from pydantic import BaseModel, ConfigDict
from typing import Optional, List
import re

# Definição do formato de dados (Schemas)

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = None
    admin: Optional[bool] = None

    # Nova sintaxe do Pydantic V2 (substitui class Config)
    model_config = ConfigDict(from_attributes=True)


class Entrada(BaseModel):
    topico_de_estudo: str
    prazo: str

    # Métodos auxiliares mantidos iguais
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
    id: int
    titulo: str
    conteudo: str
    criado_em: str

    # Nova sintaxe do Pydantic V2
    model_config = ConfigDict(from_attributes=True)


class LoginSchema(BaseModel):
    email: str
    senha: str

    # Nova sintaxe do Pydantic V2
    model_config = ConfigDict(from_attributes=True)