
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

    try {
        // 1. Limpa resultados anteriores (se existirem)
        const antigoContainer = document.getElementById("roteiro-container");
        if (antigoContainer) antigoContainer.remove();

        // 2. Pega os dias de estudo da API
        // data.agenda[0].dias_de_estudo é o teu array de strings, ex: ["Dia 1: Tópico..."]
        const dias = data.agenda[0].dias_de_estudo;

        // 3. Cria o "card" principal que vai segurar tudo
        const roteiroCard = document.createElement("div");
        roteiroCard.id = "roteiro-container";
        roteiroCard.className = "roteiro-card"; // Classe para o CSS

        // 4. Adiciona o HTML do título e da barra de progresso (ainda estática)
        // Usamos 'innerHTML' para construir o esqueleto do card
        roteiroCard.innerHTML = `
            <h2>Seu roteiro personalizado</h2>
            <div class="roteiro-progresso">
                <span id="progresso-texto">0/${dias.length} dias concluídos</span>
                <div class="progresso-barra">
                    <div id="progresso-preenchimento" class="progresso-preenchimento" style="width: 0%;"></div>
                </div>
            </div>
        `;

        // 5. Cria o container para a lista de checkboxes
        const listaContainer = document.createElement("div");
        listaContainer.className = "roteiro-lista";

        // 6. Faz um loop nos dias de estudo e cria um item de checkbox para cada um
        dias.forEach((dia, index) => {
            // 'dia' é a string completa, ex: "Dia 1: Revisão de Funções..."
            // 'index' é o número (0, 1, 2...)
            const itemId = `roteiro-item-${index}`;

            // Cria o HTML para cada item da lista
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