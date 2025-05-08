document.addEventListener('DOMContentLoaded', carregarCarrinho);

async function carregarCarrinho() {
    try {
        const response = await fetch('/carrinho/obter/');
        const data = await response.json();

        if (data.sucesso) {
            exibirItensCarrinho(data.carrinho.itens);
            atualizarResumo(data.carrinho.itens);
        } else {
            alert(data.erro);
        }
    } catch (error) {
        console.error('Erro ao carregar carrinho:', error);
        alert('Erro ao carregar carrinho.');
    }
}

function exibirItensCarrinho(itens) {
    const listaItensCarrinho = document.getElementById('lista-itens-carrinho');
    const carrinhoVazio = document.querySelector('.carrinho-vazio');
    listaItensCarrinho.innerHTML = '';

    if (itens.length === 0) {
        carrinhoVazio.style.display = 'block';
    } else {
        carrinhoVazio.style.display = 'none';

        itens.forEach(item => {
            const li = document.createElement('li');
            li.classList.add('carrinho-item');
            li.innerHTML = `
                <div class="item-imagem">
                    <img src="${item.produto.imagem}" alt="${item.produto.nome}">
                </div>
                <div class="item-detalhes">
                    <h4 class="item-nome">${item.produto.nome}</h4>
                    <p class="item-preco">R$ ${item.produto.preco.toFixed(2)}</p>
                </div>
                <div class="item-quantidade">
                    <label for="quantidade-${item.produto.id}">Qtd:</label>
                    <input type="number" id="quantidade-${item.produto.id}" value="${item.quantidade}" min="1"
                           data-produto-id="${item.produto.id}" onchange="atualizarQuantidade(this)">
                </div>
                <div class="item-total">
                    <strong>R$ ${(item.produto.preco * item.quantidade).toFixed(2)}</strong>
                </div>
                <div class="item-remover">
                    <button class="remover-item" data-produto-id="${item.produto.id}" onclick="removerItem(this)">Remover</button>
                </div>
            `;
            listaItensCarrinho.appendChild(li);
        });
    }
}

function atualizarResumo(itens) {
    const subtotalElement = document.getElementById('subtotal');
    const totalElement = document.getElementById('total');
    let subtotal = 0;

    itens.forEach(item => {
        subtotal += item.produto.preco * item.quantidade;
    });

    const frete = 0;
    const total = subtotal + frete;

    subtotalElement.textContent = `R$ ${subtotal.toFixed(2)}`;
    totalElement.textContent = `R$ ${total.toFixed(2)}`;
}

async function atualizarQuantidade(input) {
    const produtoId = input.dataset.produtoId;
    const quantidade = parseInt(input.value);

    try {
        const response = await fetch('/carrinho/atualizar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ produto_id: produtoId, quantidade: quantidade })
        });

        const data = await response.json();

        if (data.sucesso) {
            carregarCarrinho();  // Recarrega carrinho atualizado
        } else {
            alert(data.erro || 'Erro ao atualizar item.');
            input.value = input.defaultValue;
        }
    } catch (error) {
        console.error('Erro ao atualizar quantidade:', error);
        alert('Erro ao atualizar quantidade.');
        input.value = input.defaultValue;
    }
}

async function removerItem(button) {
    const produtoId = button.dataset.produtoId;

    try {
        const response = await fetch('/carrinho/remover/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ produto_id: produtoId })
        });

        const data = await response.json();

        if (data.sucesso) {
            carregarCarrinho();
        } else {
            alert(data.erro || 'Erro ao remover item.');
        }
    } catch (error) {
        console.error('Erro ao remover item:', error);
        alert('Erro ao remover item.');
    }
}

function finalizarCompra() {
    alert('Finalizar Compra - Implemente sua lógica aqui.');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function finalizarCompra() {
    try {
        const response = await fetch('/carrinho/finalizar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (data.sucesso) {
            alert('Compra finalizada com sucesso!');
            window.location.href = data.redirect || '/catalogo/';  // ou página de agradecimento
        } else {
            alert(data.erro || 'Erro ao finalizar compra.');
        }
    } catch (error) {
        console.error('Erro ao finalizar compra:', error);
        alert('Erro ao finalizar compra.');
    }
}
