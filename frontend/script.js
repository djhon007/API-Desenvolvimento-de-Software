// PASSO 1: "GUARDA DE ROTA" (Page Guard)
// executado assim que o script.js é carregado
// verificar se o token existe no localStorage
const token = localStorage.getItem("access_token");

if (!token) {
    // Se NÃO houver token...
    alert("Acesso negado. Por favor, faça o login.");
    // Redireciona o utilizador IMEDIATAMENTE para a página de login.
    window.location.href = "login.html";
}

// PASSO 2: CORREÇÃO DA URL DA API
// rota do backend é /rotinas/gerar-agenda
const URL = "http://127.0.0.1:8000/rotinas/gerar-agenda";

// PASSO 3: MODIFICAÇÃO DA FUNÇÃO GerarAgenda
// função original, agora com o cabeçalho de Autenticação
async function GerarAgenda(){

    //pegando oque o usuario digitou
    const topico = document.getElementById("Topico_estudo").value;
    const prazo = document.getElementById("Prazo").value;

    //criando o corpo
    const body = {
        topico_de_estudo: topico,
        prazo: prazo
    }
    
    //defindindo comunicacao do front com o back
    const init = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            // 
            // *** AQUI ESTÁ A MAGIA! ***
            // Estamos a enviar o token que guardámos no login.
            //
            "Authorization": "Bearer " + token 
        },
        body: JSON.stringify(body)
    }
    console.log(URL)

    try {
        //chamar o post na api
        const response = await fetch(URL,init)

        // Verificar se o token expirou (ou é inválido)
        if (response.status === 401) {
            alert("Sua sessão expirou. Por favor, faça login novamente.");
            localStorage.removeItem("access_token"); // Limpa o token antigo
            window.location.href = "login.html";
            return; // Para a execução
        }

        if (!response.ok) {
            // Se der outro erro (ex: 422, 500)
            const errorData = await response.json();
            alert(`Ocorreu um erro ao gerar o roteiro: ${errorData.detail || 'Tente novamente.'}`);
            return; // Para a execução
        }

        //converter para json
        const data = await response.json();

        // mostrar o retorno na tela
        // (O teu código original para mostrar o resultado, está perfeito)
        const antigo = document.getElementById("resultado");
        if (antigo) antigo.remove();

        const container = document.createElement("div");
        container.id = "resultado";
        container.innerHTML = `<h2> Plano de Estudos Gerado:</h2>`;

        // (Nota: o teu backend parece devolver a agenda dentro de uma lista,
        // Vou manter o teu código original que acede a data.agenda[0].dias_de_estudo)
        console.log("Resposta completa da API:", data);

        // transforma o conteúdo em linhas separadas
        const dias = data.conteudo.split("\n");


        const lista = document.createElement("ul");
        lista.style.listStyle = "none";
        lista.style.padding = "0";

        dias.forEach((dia) => {
            const item = document.createElement("li");
            item.textContent = dia;
            item.style.margin = "8px 0";
            item.style.padding = "10px";
            item.style.borderRadius = "6px";
            item.style.background = "#F0F9FF";
            item.style.border = "1px solid #BEE3F8";
            item.style.fontFamily = "Roboto, sans-serif";
            lista.appendChild(item);
        });

        container.appendChild(lista);
        // Adiciona o resultado logo abaixo do container principal
        document.querySelector("main").appendChild(container);


    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Não foi possível conectar ao servidor.");
    }
}

// Ligar o botão à função
document.getElementById("botao_gerar_roteiro").addEventListener("click", (e) => {
    e.preventDefault(); // Impede o link '#' de navegar
    GerarAgenda();
});

// PASSO 4: FUNÇÃO DE LOGOUT
// função será ligada a um novo botão no index.html
function fazerLogout() {
    localStorage.removeItem("access_token"); // Limpa o token
    alert("Logout realizado com sucesso.");
    window.location.href = "login.html"; // Envia para o login
}