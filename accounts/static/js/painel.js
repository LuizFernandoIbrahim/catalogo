document.addEventListener("DOMContentLoaded", () => {
    console.log("JS do painel carregado");

    const form = document.getElementById("product-form");
    const productList = document.getElementById("product-list");

    // Função utilitária para obter o token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Submissão do formulário
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const data = {
            nome: document.getElementById("product-name").value,
            preco: parseFloat(document.getElementById("product-price").value),
            imagem: document.getElementById("product-image").value,
            categoria: document.getElementById("product-category").value,
            descricao: document.getElementById("product-description").value,
        };

        fetch("/adicionar-produto/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(result => {
            if (result.sucesso) {
                alert("Produto adicionado com sucesso!");
                form.reset();
                // Você pode também recarregar ou re-renderizar a lista com fetch de produtos aqui
                window.location.reload();
            } else {
                alert("Erro: " + result.erro);
            }
        })
        .catch(error => {
            console.error("Erro ao adicionar produto:", error);
            alert("Ocorreu um erro inesperado.");
        });
    });
});