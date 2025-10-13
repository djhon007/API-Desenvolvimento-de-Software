# Guia de Contribuição - Projeto [Lumin]

Este documento serve como nosso guia central para a colaboração no projeto. 
O objetivo é manter nosso repositório organizado, nosso código consistente e nosso fluxo de trabalho eficiente. 
Por favor, leia e use-o como referência.

## Sumário
1.  [Configuração do Ambiente Local](#1-configuração-do-ambiente-local)
2.  [Passo a passo: Como abrir uma issue no repositório](#2-passo-a-passo-como-abrir-uma-issue-no-repositório)
3.  [Convenções para versionamento](#3-convenções-para-versionamento)
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
4. Ative um ambiente virtual(no Linux)
   ```bash
    source venv/bin/activate
    ```
5.  Instale as dependências:
    ```bash
    pip install fastapi uvicorn google-genai python-dotenv pydantic
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
### 2. Passo a passo: Como abrir uma issue no repositório

1. Vá até a página principal do repositório no GitHub.

2. Clique na aba "Issues" no topo da página.

3. Clique no botão verde "New Issue" (Nova Issue).

4. No campo "Title" (Título), escreva um título claro e objetivo sobre o problema ou sugestão.

## Exemplos:

Bug: erro ao enviar formulário de contato

Sugestão: adicionar botão de logout

## No campo de descrição, inclua:

1. Uma explicação detalhada do problema ou sugestão

2. Se for um bug, descreva os passos para reproduzir o erro

3. Se possível, inclua prints de tela ou mensagens de erro

4. (Opcional) Adicione labels como bug, enhancement, question, se você tiver permissão.

5. Clique em "Submit new issue" para criar a issue.

### 3. Convenções para versionamento
