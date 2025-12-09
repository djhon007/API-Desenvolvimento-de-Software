const BASE_URL = "https://api-desenvolvimento-de-software-production.up.railway.app";

document.addEventListener("DOMContentLoaded", () => {
    
    const loginForm = document.getElementById("login-form");
    const messageElement = document.getElementById("form-message");

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault(); 

        messageElement.textContent = "";
        messageElement.className = "";

        const email = document.getElementById("email").value;
        const senha = document.getElementById("senha").value;

        const URL = `${BASE_URL}/auth/login-form`;

        const body = new URLSearchParams();
        body.append('username', email); 
        body.append('password', senha); 

        const init = {
            method: 'POST',
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: body
        };

        try {
            const response = await fetch(URL, init);

            if (response.ok) {
                const data = await response.json();
                
                localStorage.setItem("access_token", data.access_token);

                messageElement.textContent = "Login bem-sucedido! A redirecionar...";
                messageElement.className = "success";

                setTimeout(() => {
                    window.location.href = "index.html";
                }, 1500);

            } else {
                const errorData = await response.json();
                
                let errorMessage = errorData.detail || "Email ou senha inválidos.";
                
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
