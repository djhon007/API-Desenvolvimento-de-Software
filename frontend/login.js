document.addEventListener("DOMContentLoaded", () => {
    
    const loginForm = document.getElementById("login-form");
    const messageElement = document.getElementById("form-message"); // O nosso elemento de mensagem

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault(); 

        messageElement.textContent = "";
        messageElement.className = "";

        // 1. Obter valores
        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        // 2. Definir o endpoint
        const URL = "http://127.0.0.1:8000/auth/login-form";

        // 3. Configurar o body
        // O endpoint /login-form espera dados de formulário
        const body = new URLSearchParams();
        body.append('username', email); // O FastAPI (OAuth2PasswordRequestForm) usa 'username' para o email
        body.append('password', senha); // E 'password' para a senha

        // 4. Configurar o fetch
        const init = {
            method: 'POST',
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: body
        };

        // 5. Tentar fazer a chamada
        try {
            const response = await fetch(URL, init);

            if (response.ok) {
                // SUCESSO!
                const data = await response.json();
                
                // 6. GUARDAR O TOKEN!
                localStorage.setItem("access_token", data.access_token);

                // 7. Redirecionar para a página principal
                // (Mostra uma mensagem de sucesso primeiro)
                messageElement.textContent = "Login bem-sucedido! A redirecionar...";
                messageElement.className = "success";

                setTimeout(() => {
                    window.location.href = "index.html"; // A tua página da app!
                }, 1500); // 1.5 segundos

            } else {
                // ERRO! (Ex: senha errada)
                const errorData = await response.json();
                
                // O FastAPI/OAuth2 devolve o erro em "detail"
                let errorMessage = errorData.detail || "Email ou senha inválidos.";
                
                // O FastAPI usa "INVALID_GRANT_ERROR" para login falhado
                if (errorMessage === "INVALID_GRANT_ERROR") {
                    errorMessage = "Email ou senha inválidos.";
                }

                messageElement.textContent = `Erro: ${errorMessage}`;
                messageElement.className = "error";
            }
        } catch (error) {
            console.error("Erro na requisição:", error);
            messageElement.textContent = "Não foi possível conectar ao servidor.";
            messageElement.className = "error";
        }
    });
});