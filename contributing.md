# 🧭 Guia de Contribuição – Projeto Lumin

Este documento serve como o guia central de colaboração no projeto **Lumin**. O objetivo é manter o repositório organizado, o código consistente e o fluxo de trabalho eficiente. Utilize-o como referência para contribuir com segurança e qualidade.

---

## Sumário

1. [Configuração do Ambiente Local](#1-configuração-do-ambiente-local)
2. [Passo a passo: Como abrir uma issue](#2-passo-a-passo-como-abrir-uma-issue)
3. [Convenções de Versionamento](#3-convenções-de-versionamento)
4. [Processo de Pull Request (PR)](#4-processo-de-pull-request-pr)

---

## 1. Configuração do Ambiente Local

Para começar a desenvolver, siga os passos abaixo.

### Pré-requisitos

* **Python 3.10+**
* Bibliotecas principais:

  * `fastapi`
  * `uvicorn`
  * `pydantic`
  * `google-genai`
  * `python-dotenv`
  * `sqlalchemy`
  * `alembic`
  * `passlib[bcrypt]`

### Instalação Passo a Passo

1. Clone o repositório para sua máquina:

   ```bash
   git clone https://github.com/djhon007/API-Desenvolvimento-de-Software.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd API-Desenvolvimento-de-Software
   ```

3. Crie um ambiente virtual:

   ```bash
   python -m venv env
   ```

4. Ative o ambiente virtual (Linux/Mac):

   ```bash
   source venv/bin/activate
   ```

   *(No Windows use: `venv\Scripts\activate`)*

5. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

6. Crie o arquivo `.env` na pasta raiz e adicione suas chaves:

   ```bash
   GENAI_API_KEY="sua_chave_aqui"
   SECRET_KEY="sua_senha_aqui"
   ```

7. Execute o servidor backend:

   ```bash
   uvicorn main:app --reload
   ```

8. Em outro terminal, rode o frontend (caso exista):

   ```bash
   python3 -m http.server 8080
   ```

9. Acesse o projeto em:
   [http://127.0.0.1:8080](http://127.0.0.1:8080)

---

## 2. Passo a passo: Como abrir uma Issue

1. Vá até a página principal do repositório no **GitHub**.
2. Clique na aba **Issues** no topo da página.
3. Clique em **New Issue** (botão verde).
4. No campo **Title**, insira um título claro e objetivo.

### Exemplos de Títulos:

* `bug: erro ao enviar formulário de contato`
* `feat: adicionar botão de logout`

### Na descrição, inclua:

* Explicação detalhada do problema ou sugestão.
* Se for bug, descreva os passos para reproduzir.
* Prints de tela ou mensagens de erro (se aplicável).
* Labels apropriadas (`bug`, `enhancement`, `question`).

Finalize clicando em **Submit new issue**.

---

## 3. Convenções de Versionamento

Adotamos o padrão **Conventional Commits**.

### Formato

```bash
<type>[optional scope]: <description>

[optional body]
[optional footer(s)]
```

### Tipos de Commits

| Tipo         | Uso                                        |
| ------------ | ------------------------------------------ |
| **feat**     | Nova funcionalidade                        |
| **fix**      | Correção de bug                            |
| **docs**     | Mudanças na documentação                   |
| **style**    | Ajustes de formatação (sem alterar lógica) |
| **refactor** | Melhoria no código sem mudar comportamento |
| **test**     | Adição ou correção de testes               |
| **chore**    | Tarefas auxiliares (build, configs, etc)   |
| **perf**     | Otimizações de desempenho                  |
| **ci**       | Ajustes no pipeline (CI/CD)                |

### Exemplos

```bash
feat/login-flow
fix/signup-validation
refactor/ui-components
chore/add-ci-workflow
```

### Checklist de Qualidade

* Código executa localmente sem erros.
* Nenhum `print` ou `console.log` desnecessário.
* `.env`, `__pycache__`, `node_modules` no `.gitignore`.
* Mensagem de commit segue o padrão.
* Branch com nome descritivo.

### Regras Gerais

1. Cada branch deve tratar **apenas uma** funcionalidade.
2. Atualize sua `main` antes de criar uma nova branch:

   ```bash
   git pull origin main
   ```
3. Após testar localmente, abra um **Pull Request** (PR).
4. O **merge** só deve ocorrer após revisão e aprovação.

---

## 4. Processo de Pull Request (PR)

O PR (Pull Request) é a etapa de submissão e revisão das mudanças.

### Preparação para o PR

1. Atualize sua branch principal:

   ```bash
   git checkout main
   git pull origin main
   ```
2. Traga as atualizações para sua branch de funcionalidade:

   ```bash
   git checkout sua-branch
   git rebase main
   # ou git merge main
   ```
3. Revise seu código usando o checklist da Seção 3.

### Abrindo o PR

1. Suba sua branch:

   ```bash
   git push origin nome-da-sua-branch
   ```
2. Vá ao GitHub e abra o Pull Request.
3. Preencha o template com clareza:

   * **Título:** siga o padrão *Conventional Commits* (ex: `feat: adicionar login`).
   * **Descrição:**

     * O que este PR faz?
     * Por que a mudança é necessária?
     * Como testar?
   * **Vincule Issues:** `Resolve #42` ou `Fecha #15`.

### Revisão e Merge

* Aguarde a revisão de um membro da equipe.
* Responda aos feedbacks e envie ajustes, se necessários.
* Após aprovação e sucesso no CI/CD, o mantenedor fará o merge para a `main`.

---

## Dicas Finais

* Use commits pequenos e descritivos.
* Escreva código limpo e documentado.
* Priorize clareza e colaboração.

---

