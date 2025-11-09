from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# criar conexao do banco
db = create_engine("sqlite:///database/banco.db")

# cria a base do banco de dados
Base = declarative_base()

# Criar classe/tabela do banco
# usuario


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    rotinas = relationship("Rotina", back_populates="usuario")


    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

# rotinas


class Rotina(Base):
    __tablename__ = "rotinas"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String)
    conteudo = Column("conteudo", String)
    criado_em = Column("criado_em", String)
    concluido = Column("concluido", Boolean, default=False)

    id_usuario = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", back_populates="rotinas")
    def __init__(self, titulo, conteudo, criado_em, id_usuario):
        self.titulo = titulo
        self.conteudo = conteudo
        self.criado_em = criado_em
        self.id_usuario = id_usuario


if __name__ == "__main__":
    Base.metadata.create_all(bind=db)



