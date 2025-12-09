const BASE_URL = "https://api-desenvolvimento-de-software-production.up.railway.app";

// ==========================================
// CARREGAR ROTEIROS AO ENTRAR NA PÁGINA
// ==========================================
document.addEventListener('DOMContentLoaded', async () => {
  const token = localStorage.getItem("access_token");
  const containerDePlanos = document.getElementById("grade-de-planos");

  if (!token) {
    alert("Acesso negado. Faça o login novamente.");
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/rotinas/listar`, {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
      }
    });

    if (!response.ok) {
      if (response.status === 404) {
        containerDePlanos.innerHTML =
          "<p class='page-subtitle'>Nenhum roteiro encontrado. Crie um na página 'Início'!</p>";
      } else {
        throw new Error("Erro ao buscar roteiros.");
      }
      return;
    }

    const roteiros = await response.json();
    containerDePlanos.innerHTML = '';

    // ==========================================
    // CRIAR CADA CARD
    // ==========================================
    roteiros.forEach((roteiro, index) => {
      const card = document.createElement("div");
      card.className = "plan-card";
      card.id = `card-roteiro-${roteiro.id}`;

      const totalDias = roteiro.conteudo.split("\n").length;
      const diasConcluidos = roteiro.concluido ? totalDias : 0;
      const porcentagem = (diasConcluidos / totalDias) * 100;

      const previaDias = roteiro.conteudo.split("\n").slice(0, 2);
      const dataObj = new Date(roteiro.criado_em.split(" ")[0]);
      const dataFormatada = dataObj.toLocaleDateString("pt-BR", { timeZone: "UTC" });

      const tituloFormatado =
        roteiro.titulo.charAt(0).toUpperCase() +
        roteiro.titulo.slice(1).toLowerCase();

      card.innerHTML = `
        <div class="card-header">
          <h2 class="card-title">${tituloFormatado}</h2>
          <p class="card-date">${dataFormatada}</p>
        </div>

        <div class="progress-background">
          <div class="progress-bar" style="width: ${porcentagem}%"></div>
        </div>

        <p class="card-progress-text">${diasConcluidos}/${totalDias} dias concluídos</p>

        <div class="card-tasks">
          <p class="task-item">${previaDias[0] || "..."}</p>
          <p class="task-item">${previaDias[1] || "..."}</p>
        </div>

        <a href="#" class="btn-card" data-index="${index}">Ver plano</a>
      `;

      containerDePlanos.appendChild(card);
    });

    document.querySelectorAll(".btn-card").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        e.preventDefault();
        const index = btn.dataset.index;
        const cardElement = btn.closest(".plan-card");
        abrirModalPlano(roteiros[index], cardElement);
      });
    });

  } catch (err) {
    console.error(err);
    containerDePlanos.innerHTML =
      "<p class='page-subtitle'>Ocorreu um erro ao carregar seus roteiros.</p>";
  }
});


// ==========================================
// FUNÇÃO DO MODAL
// ==========================================
function abrirModalPlano(roteiro, cardElement) {
  const modal = document.getElementById("plano-modal");
  const overlay = document.getElementById("plano-overlay");
  const token = localStorage.getItem("access_token");

  document.getElementById("plano-titulo").textContent =
    roteiro.titulo.charAt(0).toUpperCase() + roteiro.titulo.slice(1).toLowerCase();

  const dataCriacao = roteiro.criado_em ? roteiro.criado_em.split(" ")[0] : "--/--/----";
  document.getElementById("plano-data").textContent = "Criado em " + dataCriacao;

  const tarefasDiv = document.getElementById("plano-tarefas");
  tarefasDiv.innerHTML = "";

  const dias = roteiro.conteudo.split("\n");

  dias.forEach((dia, i) => {
    if (dia.trim() !== "") {
      const itemDiv = document.createElement("div");
      itemDiv.className = "roteiro-item";

      const isChecked = roteiro.concluido ? "checked" : "";

      itemDiv.innerHTML = `
        <input type="checkbox" id="modal-item-${i}" class="roteiro-checkbox" ${isChecked}>
        <label for="modal-item-${i}">
          <span class="roteiro-titulo">${dia}</span>
        </label>
      `;

      tarefasDiv.appendChild(itemDiv);
    }
  });

  const checkboxes = tarefasDiv.querySelectorAll(".roteiro-checkbox");
  const totalCheckboxes = checkboxes.length;

  const progressBar = document.getElementById("plano-progress");
  const progressText = document.getElementById("modal-progresso-texto");

  const cardProgressBar = cardElement.querySelector(".progress-bar");
  const cardProgressText = cardElement.querySelector(".card-progress-text");

  function atualizarTudo() {
    const marcados = tarefasDiv.querySelectorAll(".roteiro-checkbox:checked").length;
    const porcentagem = totalCheckboxes ? (marcados / totalCheckboxes) * 100 : 0;

    progressBar.style.width = `${porcentagem}%`;
    progressText.textContent = `${marcados}/${totalCheckboxes} concluídos`;

    cardProgressBar.style.width = `${porcentagem}%`;
    cardProgressText.textContent = `${marcados}/${totalCheckboxes} dias concluídos`;
  }

  checkboxes.forEach((cb) => cb.addEventListener("click", atualizarTudo));
  atualizarTudo();

  // ==========================================
  // CONCLUIR
  // ==========================================
  const btnConcluir = document.querySelector(".btn-concluido");

  if (btnConcluir) {
    const novoBtn = btnConcluir.cloneNode(true);
    btnConcluir.parentNode.replaceChild(novoBtn, btnConcluir);

    novoBtn.addEventListener("click", async () => {
      checkboxes.forEach((cb) => (cb.checked = true));
      atualizarTudo();

      try {
        await fetch(`${BASE_URL}/rotinas/${roteiro.id}/concluir`, {
          method: "PATCH",
          headers: { "Authorization": "Bearer " + token }
        });

        roteiro.concluido = true;
        fecharModalPlano();
      } catch {
        alert("Erro ao marcar como concluído.");
      }
    });
  }

  // ==========================================
  // EXCLUIR
  // ==========================================
  const btnExcluirModal = document.querySelector(".btn-excluir");

  if (btnExcluirModal) {
    const novoBtnExcluir = btnExcluirModal.cloneNode(true);
    btnExcluirModal.parentNode.replaceChild(novoBtnExcluir, btnExcluirModal);

    novoBtnExcluir.addEventListener("click", async () => {
      if (!confirm("Deseja realmente excluir este plano?")) return;

      try {
        const response = await fetch(`${BASE_URL}/rotinas/${roteiro.id}/excluir`, {
          method: "DELETE",
          headers: { "Authorization": "Bearer " + token }
        });

        if (response.ok) {
          cardElement.remove();
          fecharModalPlano();
        } else {
          alert("Erro ao excluir plano.");
        }
      } catch {
        alert("Erro de conexão ao excluir.");
      }
    });
  }

  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");

  document.getElementById("close-plano").onclick = fecharModalPlano;
  overlay.onclick = fecharModalPlano;

  const btnSair = document.querySelector(".btn-sair");
  if (btnSair) btnSair.onclick = fecharModalPlano;
}


// ==========================================
// FECHAR MODAL
// ==========================================
function fecharModalPlano() {
  document.getElementById("plano-modal").classList.add("hidden");
  document.getElementById("plano-overlay").classList.add("hidden");
}
