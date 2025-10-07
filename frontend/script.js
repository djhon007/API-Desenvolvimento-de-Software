const URL = "http://127.0.0.1:8000/gerar-agenda";





async function GerarAgenda(){

    //pegando oque o usuario digitou
    const topico = document.getElementById("Topico_estudo").value;
    const prazo = document.getElementById("Prazo").value;

    //criando o corpo
    const body = {
        topico_de_estudo: topico,
        prazo: prazo
    }
    
    //defindindo comunicacao do front com o back
    const init = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body)
    }

    //chamar o post na api
    const response = await fetch(URL,init)

    //converter para json
    const data = await response.json();

// mostrar o retorno na tela
// limpar resultados anteriores (se o usuario apertar duas vezes, ele nao imprime duas vezes na tela)
const antigo = document.getElementById("resultado");
if (antigo) antigo.remove();

// criar container
const container = document.createElement("div");
container.id = "resultado";
container.innerHTML = `<h2> Plano de Estudos Gerado:</h2>`;

// acessar os dias de estudo
const dias = data.agenda[0].dias_de_estudo;

// criar lista
const lista = document.createElement("ul");
lista.style.listStyle = "none";
lista.style.padding = "0";

dias.forEach((dia) => {
    const item = document.createElement("li");
    item.textContent = dia;
    item.style.margin = "8px 0";
    item.style.padding = "10px";
    item.style.borderRadius = "6px";
    item.style.background = "#F0F9FF";
    item.style.border = "1px solid #BEE3F8";
    item.style.fontFamily = "Roboto, sans-serif";
    lista.appendChild(item);
});

container.appendChild(lista);
document.body.appendChild(container);

}

// Ligar o botão à função
document.getElementById("botao_gerar_roteiro").addEventListener("click", GerarAgenda);