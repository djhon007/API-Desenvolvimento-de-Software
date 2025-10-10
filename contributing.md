# Guia de Contribuição - Projeto [Lumin]

Este documento serve como nosso guia central para a colaboração no projeto. 
O objetivo é manter nosso repositório organizado, nosso código consistente e nosso fluxo de trabalho eficiente. 
Por favor, leia e use-o como referência.

## Sumário
1.  [Configuração do Ambiente Local](#1-configuração-do-ambiente-local)
---

### 1. Configuração do Ambiente Local

Para começar a desenvolver, siga os passos abaixo:

**Pré-requisitos:**
* Python 3.10
* Bibliotecas: Pydantic, google, fastapi, goole-generativeai

**Instalação:**
1.  Clone o repositório para sua máquina:
    ```bash
    git clone [https://github.com/djhon007/API-Desenvolvimento-de-Software.git]
    ```

2.  Navegue até o diretório do projeto:
    ```bash
    cd [API-Desenvolvimento-de-Software]
    ```
3. Crie um ambiente virtual
   ```bash
    python -m venv env
    ```
5.  Instale as dependências:
    ```bash
    pip install pydantic google-generativeai fastapi google
    ```
6. Crie um arquivo ".env" na pasta do projeto e inserir uma chave de API gemini válida
```bash
    GENAI+API+KEY="sua_chave_aqui"
```
7. Digite no terminal o seguinte comando:
   ```bash
    uvicorn main:app --reload
    ```
8. Abra um outro terminal na pasta "frontend" e digite o comando:
   ```bash
    python3 -m http.server 8080
    ```
9. Abrir o link:
    http://127.0.0.1:8080
**Comandos Úteis:**
