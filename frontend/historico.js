document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem("access_token");
  const containerDePlanos = document.getElementById("grade-de-planos");

  if (!token) {
    alert("Acesso negado. Por favor, faça o login.");
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:8000/rotinas/listar", {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      }
    });

    if (response.status === 401) {
      alert("Sessão expirada. Faça login novamente.");
      localStorage.removeItem("access_token");
      window.location.href = "login.html";
      return;
    }

    if (!response.ok) {
      if (response.status === 404) {
        containerDePlanos.innerHTML = "<p class='page-subtitle'>Nenhum roteiro encontrado. Crie um na página 'Início'!</p>";
      } else {
        throw new Error('Falha ao buscar roteiros.');
      }
      return;
    }

    const roteiros = await response.json();
    containerDePlanos.innerHTML = '';

    roteiros.forEach((roteiro, index) => {
      const cardDiv = document.createElement('div');
      cardDiv.className = 'plan-card';
      // Damos um ID ao card para facilitar a busca depois, se precisar
      cardDiv.id = `card-roteiro-${roteiro.id}`;

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
          <p class="card-date">${dataFormatada}</p>
        </div>
        <div class="progress-background">
          <div class="progress-bar" style="width: ${percentagem}%;"></div>
        </div>
        <p class="card-progress-text">${diasConcluidos}/${totalDias} dias concluídos</p>
        
        <div class="card-tasks">
          <p class="task-item">${previaDias[0] || '...'}</p>
          <p class="task-item">${previaDias[1] || '...'}</p>
        </div>
        
        <a href="#" class="btn-card" data-index="${index}">Ver plano</a>
      `;
      containerDePlanos.appendChild(cardDiv);
    });

    // Ativa os botões "Ver plano"
    document.querySelectorAll('.btn-card').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const index = e.target.dataset.index;
        // O segredo: Passamos o roteiro E o elemento do card (o pai do botão)
        const cardElement = e.target.closest('.plan-card');
        abrirModalPlano(roteiros[index], cardElement);
      });
    });

  } catch (error) {
    console.error("Erro ao carregar roteiros:", error);
    containerDePlanos.innerHTML = "<p class='page-subtitle'>Ocorreu um erro ao carregar seus roteiros.</p>";
  }
});

// --- FUNÇÃO DO MODAL ATUALIZADA ---
function abrirModalPlano(roteiro, cardElement) {
  const modal = document.getElementById('plano-modal');
  const overlay = document.getElementById('plano-overlay');
  const token = localStorage.getItem("access_token");

  // 1. Preenche dados básicos
  const tituloFormatado = roteiro.titulo.charAt(0).toUpperCase() + roteiro.titulo.slice(1).toLowerCase();
  document.getElementById('plano-titulo').textContent = tituloFormatado;
  
  const dataCriacao = roteiro.criado_em ? roteiro.criado_em.split(' ')[0] : '--/--/----';
  document.getElementById('plano-data').textContent = "Criado em " + dataCriacao;

  // 2. Gera Checkboxes
  const tarefasDiv = document.getElementById('plano-tarefas');
  tarefasDiv.innerHTML = '';
  
  const dias = roteiro.conteudo.split('\n');

  dias.forEach((dia, index) => {
    if (dia.trim() !== '') {
      const itemId = `modal-item-${index}`;
      const itemDiv = document.createElement('div');
      itemDiv.className = 'roteiro-item'; 

      // Se o roteiro já estiver 100% concluído no banco, marca tudo
      const isChecked = roteiro.concluido ? 'checked' : '';

      itemDiv.innerHTML = `
          <input type="checkbox" id="${itemId}" class="roteiro-checkbox" ${isChecked}>
          <label for="${itemId}">
              <span class="roteiro-titulo">${dia}</span>
          </label>
      `;
      tarefasDiv.appendChild(itemDiv);
    }
  });

  // 3. Sincronização Visual (Modal <-> Card)
  const progressBarModal = document.getElementById('plano-progress');
  const progressTextModal = document.getElementById('modal-progresso-texto');
  const checkboxes = tarefasDiv.querySelectorAll('.roteiro-checkbox');
  const totalCheckboxes = checkboxes.length;

  // Elementos do Card de trás (que vamos atualizar)
  const cardProgressBar = cardElement.querySelector('.progress-bar');
  const cardProgressText = cardElement.querySelector('.card-progress-text');

  function atualizarTudo() {
      const marcados = tarefasDiv.querySelectorAll('.roteiro-checkbox:checked').length;
      const porcentagem = totalCheckboxes > 0 ? (marcados / totalCheckboxes) * 100 : 0;
      
      // Atualiza Modal
      progressBarModal.style.width = `${porcentagem}%`;
      progressTextModal.textContent = `${marcados}/${totalCheckboxes} concluídos`;

      // Atualiza Card (Lá no fundo)
      if(cardProgressBar) cardProgressBar.style.width = `${porcentagem}%`;
      if(cardProgressText) cardProgressText.textContent = `${marcados}/${totalCheckboxes} dias concluídos`;
  }

  // Listeners para cliques individuais
  checkboxes.forEach(cb => {
      cb.addEventListener('click', atualizarTudo);
  });

  // --- BOTÃO CONCLUÍDO (COM INTEGRAÇÃO AO BANCO) ---
  const btnConcluido = document.querySelector('.btn-concluido');
  if (btnConcluido) {
      // Truque para remover listeners antigos
      const novoBtn = btnConcluido.cloneNode(true);
      btnConcluido.parentNode.replaceChild(novoBtn, btnConcluido);
      
      novoBtn.addEventListener('click', async () => {
          // 1. Visualmente marca tudo
          checkboxes.forEach(cb => cb.checked = true);
          atualizarTudo();

          // 2. Envia para o Backend (SALVAR NO BANCO)
          try {
              const response = await fetch(`http://127.0.0.1:8000/rotinas/${roteiro.id}/concluir`, {
                  method: 'PATCH',
                  headers: {
                      "Authorization": "Bearer " + token
                  }
              });

              if (response.ok) {
                  // Atualiza o objeto local também para não perder se fechar e abrir
                  roteiro.concluido = true; 
                  fecharModalPlano();
              } else {
                  alert("Erro ao salvar a conclusão no sistema.");
              }
          } catch (error) {
              console.error(error);
              alert("Erro de conexão ao tentar salvar.");
          }
      });
  }

  // Inicializa os valores ao abrir
  atualizarTudo();

  // Mostrar Modal
  modal.classList.remove('hidden');
  overlay.classList.remove('hidden');

  // Fechar
  document.getElementById('close-plano').onclick = fecharModalPlano;
  overlay.onclick = fecharModalPlano;
  const btnSair = document.querySelector('.btn-sair');
  if(btnSair) btnSair.onclick = (e) => {
      e.preventDefault();
      fecharModalPlano();
  };
}

function fecharModalPlano() {
  document.getElementById('plano-modal').classList.add('hidden');
  document.getElementById('plano-overlay').classList.add('hidden');
}