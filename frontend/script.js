const BASE_URL = "https://api-desenvolvimento-de-software-production.up.railway.app";
const token = localStorage.getItem("access_token");

if (!token) {
    alert("Acesso negado. Por favor, faça o login.");
    window.location.href = "login.html";
}

const URL = `${BASE_URL}/rotinas/gerar-agenda`;

let roteiroTemporario = null;

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

    const loadingOverlay = document.getElementById('loading-overlay'); 

    try {
        loadingOverlay.classList.remove('hidden');

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
        roteiroTemporario = data;

        const antigo = document.getElementById("roteiro-container");
        if (antigo) antigo.remove();

        const dias = data.conteudo.split("\n");

        const roteiroCard = document.createElement("div");
        roteiroCard.id = "roteiro-container";
        roteiroCard.className = "roteiro-card";

        roteiroCard.innerHTML = `
            <h2>Seu roteiro personalizado</h2>
            <div class="roteiro-progresso">
                <span id="progresso-texto">0/${dias.length} dias concluídos</span>
                <div class="progresso-barra">
                    <div id="progresso-preenchimento" class="progresso-preenchimento" style="width: 0%;"></div>
                </div>
            </div>
        `;

        const listaContainer = document.createElement("div");
        listaContainer.className = "roteiro-lista";

        dias.forEach((dia, index) => {
            const itemId = `roteiro-item-${index}`;
            const itemDiv = document.createElement("div");
            itemDiv.className = "roteiro-item";
            
            itemDiv.innerHTML = `
                <input type="checkbox" id="${itemId}" class="roteiro-checkbox">
                <label for="${itemId}">
                    <span class="roteiro-titulo">${dia}</span>
                </label>
            `;
            listaContainer.appendChild(itemDiv);
        });

        roteiroCard.appendChild(listaContainer);

        const botoesDiv = document.createElement("div");
        botoesDiv.className = "roteiro-botoes";
        botoesDiv.innerHTML = `
            <button class="btn-secundario" id="btn-salvar">Salvar</button>
        `;

        // BOTÃO SALVAR
        document.addEventListener("click", async (e) => {
            if (e.target.id === "btn-salvar") {
                const response = await fetch(`${BASE_URL}/rotinas/salvar`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + token
                    },
                    body: JSON.stringify({
                        titulo: roteiroTemporario.titulo,
                        conteudo: roteiroTemporario.conteudo
                    })
                });

                if (response.ok) {
                    alert("Roteiro salvo com sucesso!");
                    roteiroTemporario = null;
                } else {
                    alert("Erro ao salvar o roteiro.");
                }
            }
        });

        roteiroCard.appendChild(botoesDiv);

        document.querySelector("main").appendChild(roteiroCard);

        setupProgressoListeners();

    } catch (error) {
        console.error("Erro ao tentar renderizar o roteiro:", error);
        alert("Erro ao processar o roteiro recebido.");
    } finally {
        loadingOverlay.classList.add("hidden")
    }
}

const botao = document.getElementById("botao_gerar_roteiro");

if (botao) {
    botao.addEventListener("click", (e) => {
        e.preventDefault();
        GerarAgenda();
    });
} else {
    console.error("ERRO GRAVE: botão 'botao_gerar_roteiro' não encontrado");
}

function fazerLogout() {
    localStorage.removeItem("access_token"); 
    alert("Logout realizado com sucesso.");
    window.location.href = "login.html"; 
}
