const BASE_URL = "https://api-desenvolvimento-de-software-production.up.railway.app";

document.addEventListener("DOMContentLoaded", () => {
    
    const registroForm = document.getElementById("registro-form");
    const messageElement = document.getElementById("form-message"); 

    registroForm.addEventListener("submit", async (e) => {
        e.preventDefault(); 
        
        messageElement.textContent = "";
        messageElement.className = "";

        const nome = document.getElementById("nome").value;
        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        const URL = `${BASE_URL}/auth/criar_conta`;

        const body = {
            nome: nome,
            email: email,
            senha: senha,  
            ativo: true,   
            admin: false 
        };

        const init = {
            method: 'POST',
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        };

        try {
            const response = await fetch(URL, init);
            
            if (response.ok) {
                messageElement.textContent = "Conta criada com sucesso! A redirecionar para o login...";
                messageElement.className = "success"; 

                setTimeout(() => {
                    window.location.href = "login.html";
                }, 2000); 

            } else {
                const errorData = await response.json();
                
                let errorMessage = 'Não foi possível criar a conta.'; 
                
                if (errorData.detail) {
                    if (Array.isArray(errorData.detail)) {
                        errorMessage = errorData.detail.map(err => `${err.loc[1]}: ${err.msg}`).join(', ');
                    } else {
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
