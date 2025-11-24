document.addEventListener('DOMContentLoaded', async () => {


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
        
        const roteiros = await response.json(); 
        
        containerDePlanos.innerHTML = ''; 

        roteiros.forEach(roteiro => {

            const cardDiv = document.createElement('div');
            cardDiv.className = 'plan-card'; 

            const totalDias = roteiro.conteudo.split('\n').length;
            const diasConcluidos = roteiro.concluido ? totalDias : 0;
            const percentagem = (diasConcluidos / totalDias) * 100;
            
            const previaDias = roteiro.conteudo.split('\n').slice(0, 2);

            const dataObj = new Date(roteiro.criado_em.split(' ')[0]);
            const dataFormatada = dataObj.toLocaleDateString('pt-BR', { timeZone: 'UTC' });
            const tituloFormatado = roteiro.titulo.charAt(0).toUpperCase() + roteiro.titulo.slice(1).toLowerCase();

            cardDiv.innerHTML = `
                <div class="card-header">
                    <h2 class="card-title">${tituloFormatado}</h2>
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

            containerDePlanos.appendChild(cardDiv);
        });

        ativarRecursosDaPagina(roteiros);


    } catch (error) {
        console.error("Erro ao carregar roteiros:", error);
        containerDePlanos.innerHTML = "<p class='page-subtitle'>Ocorreu um erro ao carregar seus roteiros. Tente novamente mais tarde.</p>";
    }

});

function ativarRecursosDaPagina(roteiros) {

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


    const searchInput = document.querySelector('.search-input');
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
}