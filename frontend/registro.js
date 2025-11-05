document.addEventListener("DOMContentLoaded", () => {
    
    const registroForm = document.getElementById("registro-form");
    const messageElement = document.getElementById("form-message"); 

    registroForm.addEventListener("submit", async (e) => {
        e.preventDefault(); 
        
        messageElement.textContent = "";
        messageElement.className = "";

        // 1. Obter os valores (sem alteração)
        const nome = document.getElementById("nome").value;
        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        const URL = "http://127.0.0.1:8000/auth/criar_conta";

        // 
        // *** AQUI ESTÁ A CORREÇÃO FINAL ***
        // Este 'body' agora corresponde exatamente ao que o teu backend espera.
        //
        const body = {
            nome: nome,
            email: email,
            senha: senha,    // Corrigido de volta para 'senha'
            ativo: true,     // Campo obrigatório adicionado
            admin: false     // Campo obrigatório adicionado
        };

        const init = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        };

        try {
            const response = await fetch(URL, init);
            
            if (response.ok) {
                // SUCESSO!
                messageElement.textContent = "Conta criada com sucesso! A redirecionar para o login...";
                messageElement.className = "success"; 

                setTimeout(() => {
                    window.location.href = "login.html";
                }, 2000); 

            } else {
                // ERRO! (A nossa formatação de erro)
                const errorData = await response.json();
                
                let errorMessage = 'Não foi possível criar a conta.'; 
                
                if (errorData.detail) {
                    if (Array.isArray(errorData.detail)) {
                        // Ex: "Erro: email: Email já registado"
                        errorMessage = errorData.detail.map(err => `${err.loc[1]}: ${err.msg}`).join(', ');
                    } else {
                        // Ex: "Erro: Email já registado"
                        errorMessage = errorData.detail;
                    }
                }
                
                messageElement.textContent = `Erro: ${errorMessage}`;
                messageElement.className = "error"; 
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            messageElement.textContent = "Não foi possível conectar ao servidor. Tente novamente.";
            messageElement.className = "error";
        }
    });
});