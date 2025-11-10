
const token = localStorage.getItem("access_token");

if (!token) {
    alert("Acesso negado. Por favor, faça o login.");
    window.location.href = "login.html";
}

const URL = "http://127.0.0.1:8000/rotinas/gerar-agenda";

async function GerarAgenda(){

    const topico = document.getElementById("Topico_estudo").value;
    const prazo = document.getElementById("Prazo").value;

    const body = {
        topico_de_estudo: topico,
        prazo: prazo
    }
    
    const init = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",

            "Authorization": "Bearer " + token 
        },
        body: JSON.stringify(body)
    }
    console.log(URL)

    try {
        const response = await fetch(URL,init)

        if (response.status === 401) {
            alert("Sua sessão expirou. Por favor, faça login novamente.");
            localStorage.removeItem("access_token"); 
            window.location.href = "login.html";
            return; 
        }

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Ocorreu um erro ao gerar o roteiro: ${errorData.detail || 'Tente novamente.'}`);
            return; 
        }

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

        // Adiciona a lista de checkboxes ao card
        roteiroCard.appendChild(listaContainer);

        // 7. Adiciona os botões (ainda visuais, sem função)
        const botoesDiv = document.createElement("div");
        botoesDiv.className = "roteiro-botoes";
        botoesDiv.innerHTML = `
            <button class="btn-secundario">Salvar</button>
            <button class="btn-secundario">Exportar PDF</button>
            <button class="btn-secundario">Compartilhar</button>
        `;
        roteiroCard.appendChild(botoesDiv);

        // 8. Finalmente, adiciona o card completo à tua página
        // Vamos adicioná-lo dentro da tag <main>
        document.querySelector("main").appendChild(roteiroCard);

        setupProgressoListeners();

    } catch (e) {
        console.error("Erro ao tentar renderizar o roteiro:", e);
        alert("Erro ao processar o roteiro recebido.");
    }

    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Não foi possível conectar ao servidor.");
    }
}

document.getElementById("botao_gerar_roteiro").addEventListener("click", (e) => {
    e.preventDefault();
    GerarAgenda();
});

function fazerLogout() {
    localStorage.removeItem("access_token"); 
    alert("Logout realizado com sucesso.");
    window.location.href = "login.html"; 
}

function setupProgressoListeners() {
    // 1. Encontra todos os checkboxes que acabámos de criar
    const checkboxes = document.querySelectorAll(".roteiro-checkbox");
    
    // 2. Encontra os elementos da UI que queremos atualizar
    const progressoTexto = document.getElementById("progresso-texto");
    const progressoPreenchimento = document.getElementById("progresso-preenchimento");
    
    const totalDias = checkboxes.length; // O número total de dias (ex: 10)

    // 3. Esta função será chamada sempre que um checkbox for clicado
    function atualizarProgresso() {
        // Conta quantos checkboxes estão :checked (marcados)
        const diasConcluidos = document.querySelectorAll(".roteiro-checkbox:checked").length;
        
        // Calcula a percentagem
        // (diasConcluidos / totalDias) * 100
        const percentagem = (diasConcluidos / totalDias) * 100;

        // Atualiza a UI
        progressoTexto.textContent = `${diasConcluidos}/${totalDias} dias concluídos`;
        progressoPreenchimento.style.width = `${percentagem}%`;
    }

    // 4. Adiciona um "ouvinte" de clique a CADA checkbox
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("click", atualizarProgresso);
    });
}