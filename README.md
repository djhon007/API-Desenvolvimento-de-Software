

### Commit 03/11/2025 – Integração de Autenticação e Persistência de Dados

---

## Visão Geral

Este commit marca uma grande evolução do projeto **Lumin**, que deixa de ser uma API simples de geração de planos de estudo para se tornar uma **plataforma completa**, com:

* Autenticação de usuários via JWT
* Persistência de dados em banco de dados SQLite
* Estrutura modular de rotas e dependências
* Configurações centralizadas via `.env`

Além disso, o `contribuiting.md` foi atualizado para refletir o novo stack e fluxo de desenvolvimento.

---

## Estrutura do Projeto

```bash
.
├── main.py
├── rotas/
│   ├── auth.py
│   └── rotinas.py
├── codigos_apoio/
│   ├── config.py
│   ├── dependences.py
│   ├── schemas.py
│   └── security.py
├── database/
│   └── models.py
├── .env
└── contribuiting.md
```

---

## Autenticação e Autorização (`rotas/auth.py`)

Implementada autenticação completa com **JWT (JSON Web Token)**.

### Endpoints Principais

* `POST /auth/criar_conta` → Cria novo usuário com senha criptografada
* `POST /auth/login` e `/auth/login-form` → Login e geração de *access* e *refresh tokens*
* `POST /auth/refresh` → Renova o *access token*

### Tecnologias Utilizadas

* **bcrypt** → Criptografia de senha
* **python-jose** → Geração e validação de tokens JWT
* **OAuth2PasswordBearer** → Controle de sessão e autenticação via header Bearer

---

## Rotinas de Estudo (`rotas/rotinas.py`)

As rotinas agora são **associadas a usuários autenticados** e **armazenadas no banco de dados**.

### Endpoints

* `POST /rotinas/gerar-agenda` → Gera plano via Gemini e salva no banco
* `GET /rotinas/listar` → Lista todas as rotinas criadas pelo usuário logado

### Funcionalidades

* Conversão automática de prazos para dias
* Armazenamento com título, conteúdo, data e ID do usuário
* Retorno formatado via `RotinaResponse`

---

## Banco de Dados (`database/models.py`)

Implementação com **SQLAlchemy ORM** para abstração e relações.

### Tabelas Criadas

#### `Usuario`

* `id`, `nome`, `email`, `senha`, `ativo`, `admin`
* Relacionamento com `Rotina`

#### `Rotina`

* `id`, `titulo`, `conteudo`, `criado_em`, `id_usuario`

Banco padrão:

```bash
sqlite:///database/banco.db
```

---

## Configurações e Dependências

### `codigos_apoio/config.py`

Gerencia variáveis de ambiente:

```python
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
```

### `codigos_apoio/dependences.py`

* `pegar_sessao()` → Cria sessão SQLAlchemy
* `verificar_token()` → Valida JWT e retorna usuário autenticado

### `codigos_apoio/security.py`

* Implementa criptografia com `bcrypt`

---

## Atualizações no `main.py`

O arquivo principal agora é o ponto de entrada da aplicação, registrando as rotas e configurando o CORS.

```python
app.include_router(auth_router)
app.include_router(rotinas_router)
```

Permite acesso ao frontend com:

```python
allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"]
```

---

## Atualização do `contribuiting.md`

O guia foi reformulado para refletir o novo ambiente.

### Novas Dependências

* `SQLAlchemy`
* `alembic`
* `passlib[bcrypt]`

### Mudanças

* Instalação via `requirements.txt`
* Inclusão de `SECRET_KEY` no `.env`
* Simplificação das seções de PR e versionamento

---

## Arquivo `.env`

Novo formato de variáveis:

```bash
GENAI_API_KEY="sua_chave_aqui"
SECRET_KEY="sua_senha_aqui"
```

---

## Requisitos Técnicos

**Python:** 3.10+

### Dependências

```bash
fastapi
uvicorn
google-genai
python-dotenv
pydantic
sqlalchemy
alembic
passlib[bcrypt]
python-jose
```

### Instalação

```bash
pip install -r requirements.txt
```

---

## 💻 Como Rodar o Projeto

1. Criar ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Configurar o arquivo `.env`
3. Iniciar o backend:

   ```bash
   uvicorn main:app --reload
   ```
4. Iniciar o frontend (na pasta `/frontend`):

   ```bash
   python3 -m http.server 8080
   ```
5. Acessar:

   ```bash
   http://127.0.0.1:8080
   ```

---

## Autor:

* **Gabriel Mezzalira Teixeira Batista do Nascimento**

---

## Resumo das Mudanças

* Criação de `rotas/auth.py` com autenticação JWT
* Integração com SQLAlchemy e banco SQLite
* Criação de `rotas/rotinas.py` com persistência de planos
* Criptografia de senhas com bcrypt
* Refatoração do `main.py` para modularização
* Atualização do `contribuiting.md`
* Novo `.env` com `SECRET_KEY`
