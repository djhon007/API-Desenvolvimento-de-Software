const BASE_URL = "https://api-desenvolvimento-de-software-production.up.railway.app";
const token = localStorage.getItem("access_token");

if (!token) {
    alert("Acesso negado. Por favor, faça o login.");
    window.location.href = "login.html";
}

const URL = `${BASE_URL}/rotinas/gerar-agenda`;
let roteiroTemporario = null;

// ======================================================
// FUNÇÃO PRINCIPAL — GERAR ROTEIRO
// ======================================================
async function GerarAgenda() {

    const topico = document.getElementById("Topico_estudo").value;
    const prazo = document.getElementById("Prazo").value;

    const body = { topico_de_estudo: topico, prazo: prazo };

    const init = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(body)
    };

    const loadingOverlay = document.getElementById('loading-overlay');

    try {
        loadingOverlay.classList.remove('hidden');

        const response = await fetch(URL, init);

        if (response.status === 401) {
            alert("Sessão expirada. Faça login novamente.");
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Erro ao gerar o roteiro: ${errorData.detail || "Tente novamente."}`);
            return;
        }

        const data = await response.json();
        roteiroTemporario = data;

        // remover roteiro anterior
        const antigo = document.getElementById("roteiro-container");
        if (antigo) antigo.remove();

        const dias = data.conteudo.split("\n");

        // criar card principal
        const roteiroCard = document.createElement("div");
        roteiroCard.id = "roteiro-container";
        roteiroCard.className = "roteiro-card";

        roteiroCard.innerHTML = `
            <h2>Seu roteiro personalizado</h2>

            <div class="roteiro-progresso">
                <span id="progresso-texto">0/${dias.length} dias concluídos</span>
                <div class="progresso-barra">
                    <div id="progresso-preenchimento" class="progresso-preenchimento"></div>
                </div>
            </div>
        `;

        // lista dos dias
        const listaContainer = document.createElement("div");
        listaContainer.className = "roteiro-lista";

        dias.forEach((dia, index) => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "roteiro-item";

            itemDiv.innerHTML = `
                <input type="checkbox" id="roteiro-item-${index}" class="roteiro-checkbox">
                <label for="roteiro-item-${index}">
                    <span class="roteiro-titulo">${dia}</span>
                </label>
            `;

            listaContainer.appendChild(itemDiv);
        });

        roteiroCard.appendChild(listaContainer);

        // BOTÃO SALVAR APENAS
        const botoesDiv = document.createElement("div");
        botoesDiv.className = "roteiro-botoes";

        botoesDiv.innerHTML = `
            <button class="btn-secundario" id="btn-salvar">Salvar</button>
        `;

        roteiroCard.appendChild(botoesDiv);
        document.querySelector("main").appendChild(roteiroCard);

        // ativa progresso
        setupProgressoListeners();

    } catch (error) {
        console.error("Erro ao tentar renderizar o roteiro:", error);
        alert("Erro ao processar o roteiro recebido.");
    } finally {
        loadingOverlay.classList.add("hidden");
    }
}

// ======================================================
// PROGRESSO — CHECKBOXES
// ======================================================
function setupProgressoListeners() {
    const checkboxes = document.querySelectorAll(".roteiro-checkbox");
    const progressoTexto = document.getElementById("progresso-texto");
    const progressoPreenchimento = document.getElementById("progresso-preenchimento");

    const totalDias = checkboxes.length;

    function atualizarProgresso() {
        const diasConcluidos = document.querySelectorAll(".roteiro-checkbox:checked").length;
        const porcentagem = (diasConcluidos / totalDias) * 100;

        progressoTexto.textContent = `${diasConcluidos}/${totalDias} dias concluídos`;
        progressoPreenchimento.style.width = `${porcentagem}%`;
    }

    checkboxes.forEach(cb => cb.addEventListener("click", atualizarProgresso));
}

// ======================================================
// SALVAR ROTEIRO
// ======================================================
document.addEventListener("click", async (e) => {
    if (e.target.id === "btn-salvar") {

        if (!roteiroTemporario) return;

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

// ======================================================
// CLIQUE DO BOTÃO GERAR ROTEIRO
// ======================================================
const botao = document.getElementById("botao_gerar_roteiro");

if (botao) {
    botao.addEventListener("click", (e) => {
        e.preventDefault();
        GerarAgenda();
    });
} else {
    console.error("ERRO: botão 'botao_gerar_roteiro' não encontrado");
}

// ======================================================
// LOGOUT
// ======================================================
function fazerLogout() {
    localStorage.removeItem("access_token");
    alert("Logout realizado com sucesso.");
    window.location.href = "login.html";
}
