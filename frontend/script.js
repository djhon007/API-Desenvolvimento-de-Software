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

        // mostrar o retorno na tela
        const antigo = document.getElementById("resultado-container");
        if (antigo) antigo.remove();

        console.log("Resposta completa da API:", data);

        // transforma o conteúdo em linhas separadas
        const dias = data.conteudo.split("\n");

        // declarando bonitinho
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
            
            // HTML do checkbox
            itemDiv.innerHTML = `
                <input type="checkbox" id="${itemId}" class="roteiro-checkbox">
                <label for="${itemId}">
                    <span class="roteiro-titulo">${dia}</span>
                </label>
            `;
            listaContainer.appendChild(itemDiv);
        });

        // montar
        roteiroCard.appendChild(listaContainer);

        // botões (ainda visuais, sem função)
        const botoesDiv = document.createElement("div");
        botoesDiv.className = "roteiro-botoes";
        botoesDiv.innerHTML = `
            <button class="btn-secundario">Salvar</button>
            <button class="btn-secundario">Exportar PDF</button>
            <button class="btn-secundario">Compartilhar</button>
        `;
        roteiroCard.appendChild(botoesDiv);

        // diciona o card completo à página
        document.querySelector("main").appendChild(roteiroCard);
        // lógica da barra de progresso
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
        console.log("Botão encontrado no HTML!");
        
        botao.addEventListener("click", (e) => {
            e.preventDefault();
            console.log("CLIQUEI NO BOTÃO!"); 
            GerarAgenda();
        });
    } else {
        console.error("ERRO GRAVE: O JavaScript não achou o botão com id 'botao_gerar_roteiro'");
    }

function fazerLogout() {
    localStorage.removeItem("access_token"); 
    alert("Logout realizado com sucesso.");
    window.location.href = "login.html"; 
}

function setupProgressoListeners() {
    // 1. get todos os checkboxes que acabámos de criar
    const checkboxes = document.querySelectorAll(".roteiro-checkbox");
    
    // 2. get os elementos da UI que queremos atualizar
    const progressoTexto = document.getElementById("progresso-texto");
    const progressoPreenchimento = document.getElementById("progresso-preenchimento");
    
    const totalDias = checkboxes.length; // get total de dias (ex: 10)

    // 3. evento clicável
    function atualizarProgresso() {
        // get quantos checkboxes estão :checked (marcados)
        const diasConcluidos = document.querySelectorAll(".roteiro-checkbox:checked").length;
        
        // get percentagem
        const percentagem = (diasConcluidos / totalDias) * 100;

        // att UI
        progressoTexto.textContent = `${diasConcluidos}/${totalDias} dias concluídos`;
        progressoPreenchimento.style.width = `${percentagem}%`;
    }

    // 4. add "ouvinte" de clique a CADA checkbox
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("click", atualizarProgresso);
    });
}