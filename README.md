# Lumin — Plataforma de Organização Inteligente de Estudos

O **Lumin** é uma plataforma web desenvolvida para auxiliar estudantes na organização e no planejamento de estudos de forma inteligente.  
Inicialmente concebido como uma API simples de geração de planos de estudo, o projeto evoluiu para uma plataforma completa, com autenticação de usuários, persistência de dados e arquitetura modular.

O sistema é dividido em **frontend** e **backend**, implantados separadamente em ambientes de produção.

---

## Arquitetura do Projeto

O projeto segue uma arquitetura **cliente-servidor**, com separação clara entre interface e lógica de negócio.

### Componentes

- **Frontend:** aplicação web desenvolvida em HTML, CSS e JavaScript
- **Backend:** API REST desenvolvida em Python com FastAPI
- **Banco de dados:** SQLite
- **Autenticação:** JSON Web Token (JWT)

### Deploy

- **Frontend:** Vercel
- **Backend:** Railway


## Estrutura do Repositório

```text
API-Desenvolvimento-de-Software/
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── registro.html
│   ├── historico.html
│   ├── style.css
│   ├── script.js
│   ├── login.js
│   ├── registro.js
│   ├── historico.js
│   ├── imagens/
│   ├── package.json
│   └── README.md
│
├── main.py
│
├── rotas/
│   ├── auth.py
│   └── rotinas.py
│
├── codigos_apoio/
│   ├── config.py
│   ├── dependences.py
│   ├── schemas.py
│   └── security.py
│
├── database/
│   └── models.py
│
├── alembic/
├── tests/
├── logs/
├── venv/
├── .env
└── README.md

```

## Tecnologias Utilizadas

### Frontend
- HTML5  
- CSS3  
- JavaScript (Vanilla)

### Backend
- Python  
- FastAPI  
- SQLAlchemy  
- Alembic  

### Infraestrutura
- Vercel (Frontend)  
- Railway (Backend)  

---

## Autenticação e Autorização

A autenticação da aplicação é baseada em **JSON Web Token (JWT)**, garantindo acesso seguro às rotas protegidas da API.

### Principais Endpoints

- `POST /auth/criar_conta`  
  Criação de novos usuários com senha criptografada

- `POST /auth/login`  
  Login via JSON

- `POST /auth/login-form`  
  Login via formulário utilizando `OAuth2PasswordRequestForm`

- `POST /auth/refresh`  
  Renovação do token de acesso

As rotas protegidas utilizam dependências de autenticação para validação do token JWT.

---

## Build

### Frontend

O frontend utiliza apenas HTML, CSS e JavaScript puro, não sendo necessário processo de build.  
Os arquivos estão prontos para execução em ambiente de produção.

### Backend

O backend não necessita de build, sendo executado diretamente pelo servidor Python.

---

## Deploy

### Frontend — Vercel

O frontend foi implantado na plataforma **Vercel**, conectando diretamente o repositório do GitHub.

**Passos gerais:**
1. Importar o repositório na Vercel  
2. Selecionar a pasta `frontend/` como diretório raiz  
3. Manter as configurações padrão  
4. Concluir o deploy  

---

### Backend — Railway

O backend foi implantado na plataforma **Railway**.

**Passos gerais:**
1. Conectar o repositório do GitHub ao Railway  
2. Configurar as variáveis de ambiente no arquivo `.env`  
3. Definir o comando de inicialização da aplicação  
4. Publicar o serviço  

---

## Integração Frontend e Backend

O frontend consome a API REST exposta pelo backend por meio de requisições HTTP.  
A URL da API é configurada diretamente nos arquivos JavaScript do frontend.

```javascript
const BASE_URL = "https://api-desenvolvimento-de-software-production.up.railway.app";
