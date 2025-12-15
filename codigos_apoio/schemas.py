from pydantic import BaseModel
from typing import Optional, List
import re


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class Entrada(BaseModel):
    topico_de_estudo: str
    prazo: str

    def prazo_numero(self) -> int:
        match = re.search(r"\d+", self.prazo)
        return int(match.group()) if match else 0

    def prazo_unidade(self) -> str:
        match = re.search(r"[A-Za-zÀ-ÿ]+", self.prazo)
        return match.group().lower() if match else "dias"

    def tipo_planejamento(self) -> str:
        """
        Retorna:
        - 'minutos'
        - 'horas'
        - 'dias'
        """
        unidade = self.prazo_unidade()

        if unidade in ["minuto", "minutos"]:
            return "minutos"
        elif unidade in ["hora", "horas"]:
            return "horas"
        elif unidade in [
            "dia", "dias",
            "semana", "semanas",
            "mes", "mês", "meses"
        ]:
            return "dias"
        else:
            return "dias"

    def prazo_em_dias(self) -> int:
        numero = self.prazo_numero()
        unidade = self.prazo_unidade()

        if unidade in ["semana", "semanas"]:
            return numero * 7
        elif unidade in ["mes", "mês", "meses"]:
            return numero * 30
        elif unidade in ["dia", "dias"]:
            return numero
        else:
            return 0


class Saida(BaseModel):
    dias_de_estudo: List[str]


class RotinaResponse(BaseModel):
    id: int
    titulo: str
    conteudo: str
    criado_em: str

    class Config:
        from_attributes = True


class RotinaCreate(BaseModel):
    titulo: str
    conteudo: str


class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True
