/* 'DOMContentLoaded' espera o HTML carregar antes de executar o JS.
   Tornámo-lo 'async' para podermos usar 'await' para o fetch.
*/
document.addEventListener('DOMContentLoaded', async () => {

    // -----------------------------------------------------------------
    // 1. GUARDA DE ROTA E AUTENTICAÇÃO
    // -----------------------------------------------------------------
    const token = localStorage.getItem("access_token");
    const containerDePlanos = document.getElementById("grade-de-planos");

    if (!token) {
        // Se NÃO houver token, expulsa para o login
        alert("Acesso negado. Por favor, faça o login.");
        window.location.href = "login.html";
        return; // Para a execução
    }

    if (!containerDePlanos) {
        console.error("Erro fatal: Container 'grade-de-planos' não encontrado.");
        return;
    }

    // -----------------------------------------------------------------
    // 2. BUSCAR OS ROTEIROS DA API (FETCH)
    // -----------------------------------------------------------------
    try {
        const URL = "http://127.0.0.1:8000/rotinas/listar";
        const init = {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token 
            }
        };

        const response = await fetch(URL, init);

        // Se o token expirou ou é inválido
        if (response.status === 401) {
            alert("Sua sessão expirou. Por favor, faça login novamente.");
            localStorage.removeItem("access_token");
            window.location.href = "login.html";
            return;
        }

        // Se não houver roteiros (404) ou outro erro
        if (!response.ok) {
            // O backend (rotinas.py) devolve 404 se não houver roteiros
            if (response.status === 404) {
                containerDePlanos.innerHTML = "<p class='page-subtitle'>Nenhum roteiro encontrado. Crie um na página 'Início'!</p>";
            } else {
                throw new Error('Falha ao buscar roteiros.');
            }
            return; // Para a execução
        }
        
        // SUCESSO! Temos os dados.
        const roteiros = await response.json(); // Isto é uma LISTA de roteiros
        
        // -----------------------------------------------------------------
        // 3. RENDERIZAR OS CARDS DINAMICAMENTE
        // -----------------------------------------------------------------
        
        // Limpa (por via das dúvidas)
        containerDePlanos.innerHTML = ''; 

        // Faz um loop em cada roteiro que veio do backend
        roteiros.forEach(roteiro => {
            // roteiro.id, roteiro.titulo, roteiro.conteudo, roteiro.criado_em, roteiro.concluido

            // Cria uma nova div para o card
            const cardDiv = document.createElement('div');
            cardDiv.className = 'plan-card'; // Usa a classe CSS do teu colega

            // Calcula o progresso (ex: 3/14 dias)
            // (Esta é uma lógica de exemplo, pois o backend só diz 'concluido' (true/false)
            // Vamos assumir 0% se não estiver concluído e 100% se estiver)
            const totalDias = roteiro.conteudo.split('\n').length;
            const diasConcluidos = roteiro.concluido ? totalDias : 0;
            const percentagem = (diasConcluidos / totalDias) * 100;
            
            // Pega os 2 primeiros dias para mostrar na prévia
            const previaDias = roteiro.conteudo.split('\n').slice(0, 2);

            // Formata a data (ex: 08/09/2025)
            // A data vem como "2025-11-10 11:51:09"
            const dataObj = new Date(roteiro.criado_em.split(' ')[0]);
            const dataFormatada = dataObj.toLocaleDateString('pt-BR', { timeZone: 'UTC' });

            // Insere o HTML do card, usando os dados do roteiro
            cardDiv.innerHTML = `
                <div class="card-header">
                    <h2 class="card-title">${roteiro.titulo}</h2>
                    <button class="btn-menu">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/>
                        </svg>
                    </button>
                </div>
                <p class="card-date">Criado em ${dataFormatada}</p>
                
                <div class="progress-background">
                    <div class="progress-bar" style="width: ${percentagem}%;"></div>
                </div>
                <p class="card-progress-text">${diasConcluidos}/${totalDias} dias concluídos</p>

                <div class="card-tasks">
                    <p class="task-item">${previaDias[0] || '...'}</p>
                    <p class="task-item">${previaDias[1] || '...'}</p>
                </div>

                <a href="#" class="btn-card">Ver plano</a>
            `;

            // Adiciona o card novo à grade
            containerDePlanos.appendChild(cardDiv);
        });

        // -----------------------------------------------------------------
        // 4. ATIVAR OS OUTROS SCRIPTS (Filtro, Busca, etc.)
        //    (Agora que os cards existem, podemos ativar a busca)
        // -----------------------------------------------------------------
        ativarRecursosDaPagina(roteiros);


    } catch (error) {
        console.error("Erro ao carregar roteiros:", error);
        containerDePlanos.innerHTML = "<p class='page-subtitle'>Ocorreu um erro ao carregar seus roteiros. Tente novamente mais tarde.</p>";
    }

});


/* Esta função separada contém o código do teu colega (filtro, busca)
  e só será chamada DEPOIS que o fetch terminar.
*/
function ativarRecursosDaPagina(roteiros) {

    // --- 1. RECURSO: HEADER COM SOMBRA AO ROLAR ---
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

    // --- 2. RECURSO: MODAL DE FILTROS ---
    const filterButton = document.querySelector('.btn-filter');
    const filterModal = document.getElementById('filter-modal');
    const filterCloseButton = document.getElementById('filter-close-button');
    const filterOverlay = document.getElementById('filter-overlay');

    const openModal = () => {
        if (filterModal) {
            filterModal.classList.remove('hidden');
            filterOverlay.classList.remove('hidden');
        }
    }
    
    const closeModal = () => {
        if (filterModal) {
            filterModal.classList.add('hidden');
            filterOverlay.classList.add('hidden');
        }
    }
    if (filterButton) filterButton.addEventListener('click', openModal);
    if (filterCloseButton) filterCloseButton.addEventListener('click', closeModal);
    if (filterOverlay) filterOverlay.addEventListener('click', closeModal);


    // --- 3. RECURSO: BUSCA EM TEMPO REAL (AGORA FUNCIONA COM CARDS DINÂMICOS) ---
    const searchInput = document.querySelector('.search-input');
    // Não busca mais os cards do HTML, mas sim os que acabámos de criar
    const planCards = document.querySelectorAll('.plan-card'); 

    if (searchInput) {
        searchInput.addEventListener('input', (event) => {
            const searchTerm = event.target.value.toLowerCase();

            planCards.forEach(card => {
                const titleElement = card.querySelector('.card-title');
                if (titleElement) {
                    const title = titleElement.textContent.toLowerCase();
                    if (title.includes(searchTerm)) {
                        card.style.display = 'flex'; 
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    }

    // O recurso "Cálculo Dinâmico" não é mais necessário,
    // pois já calculámos o progresso ao renderizar os cards.
}