# Guia de Contribuição - Projeto [Lumin]

Este documento serve como nosso guia central para a colaboração no projeto. 
O objetivo é manter nosso repositório organizado, nosso código consistente e nosso fluxo de trabalho eficiente. 
Por favor, leia e use-o como referência.

## Sumário
1.  [Configuração do Ambiente Local](#1-configuração-do-ambiente-local)
2.  [Passo a passo: Como abrir uma issue no repositório](#2-passo-a-passo-como-abrir-uma-issue-no-repositório)
3.  [Convenções para versionamento](#3-convenções-para-versionamento)
4.  [Processo de Pull Request (PR)](#4-processo-de-pull-request-pr)
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
    GENAI_API_KEY="sua_chave_aqui"
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

#### Baseia-se na lógica de "Conventional Commits":

## Formato:

```bash
<type>[optional scope]: <description> #tipo de commit, escopo e descrição

[optional body] #corpo opcional com maior descrição

[optional footer(s)] #opcional para incluir BREAKING CHANGES
```

## Tipos:

Tipo	Uso

1. feat:	nova funcionalidade

2. fix:	correção de bug

3. docs:	mudanças em documentação

4. style:	ajustes de formatação, espaçamento, etc (sem alterar lógica)

5. refactor:	melhoria no código sem mudar comportamento

6. test:	adição ou correção de testes

7. chore:	tarefas auxiliares (build, CI/CD, configs)

8. perf:	otimizações de desempenho

9. ci:	ajustes no pipeline (GitHub Actions, Render, etc)

### Exemplos:

feat/login-flow

fix/signup-validation

refactor/ui-components

chore/add-ci-workflow


## Checklist de qualidade antes de commit/push

1. Código executa localmente sem erros

2. Nenhum console.log ou print desnecessário

3. Arquivos .env, _pycache_, node_modules estão no .gitignore

4. Mensagem de commit segue o padrão

5. Branch tem nome descritivo

## Regras gerais

1. Cada branch deve tratar uma única mudança ou funcionalidade.

2. Antes de criar uma branch, puxe as atualizações da main (git pull origin main).

3. Após finalizar e testar localmente, abra um Pull Request descrevendo a mudança.

4. O merge deve ser feito apenas após revisão e aprovação.

### 4. Processo de Pull Request (PR)
O Pull Request (PR) é como você propõe suas mudanças ao repositório principal. É uma oportunidade para revisar o código e discutir as alterações antes de integrá-las à branch main.

Preparação para o PR
Atualize sua Base: Antes de enviar seu código, certifique-se de que sua branch main local está atualizada com a main remota:

```Bash

git checkout main
git pull origin main
```
Traga as Atualizações: Volte para sua branch de funcionalidade e traga as atualizações da main (caso haja alguma). Isso ajuda a evitar conflitos de merge.

```Bash

git checkout sua-branch
git rebase main 
# ou 'git merge main', dependendo do fluxo de trabalho preferido
```
Revise seu Trabalho: Verifique seu código pela última vez usando o Checklist de qualidade (descrito na Seção 3). Garanta que os testes passam localmente e que não há prints ou console.logs desnecessários.

Abrindo o Pull Request
Envie sua Branch: Suba sua branch para o repositório remoto:

```Bash

git push origin nome-da-sua-branch
```
Abra o PR: Vá até a página do repositório no GitHub. Você verá um aviso para abrir um Pull Request da sua branch recém-enviada. Clique nele.

#### Preencha o Template do PR: A clareza é fundamental.

Título: O título do PR deve ser claro e, idealmente, seguir o padrão de Conventional Commits (ex: feat: Adiciona rota de login ou fix: Corrige validação de e-mail).

Descrição: Use o corpo do PR para detalhar o que foi feito. Um bom formato inclui:

O que este PR faz? (Descreva as mudanças em alto nível.)

Por que esta mudança é necessária? (Qual problema ela resolve?)

Como testar? (Liste os passos para que o revisor possa validar sua implementação.)

Vincule a Issue: Se o seu PR resolve uma Issue existente (da Seção 2), use palavras-chave na descrição para vinculá-la.

Exemplo: Resolve #42 ou Fecha #15.

Revisão e Merge
Aguarde a Revisão: Um ou mais membros da equipe revisarão seu código.

Responda aos Feedbacks: É comum que os revisores solicitem alterações (ajustes de estilo, correções de lógica, mais testes). Faça os commits necessários na sua branch e envie-os (git push). O PR será atualizado automaticamente.

Aprovação e Merge: Uma vez que o PR for aprovado e passar em quaisquer verificações automáticas (CI/CD), ele estará pronto para ser "mergeado" na main pelo mantenedor do projeto.
