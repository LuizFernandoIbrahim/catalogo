document.addEventListener("DOMContentLoaded", () => {
    console.log("JS carregado");

    const form = document.getElementById("product-form");
    const productList = document.getElementById("product-list");

    let products = JSON.parse(localStorage.getItem("products")) || [];

    function renderProducts() {
        productList.innerHTML = "";
        products.forEach((product, index) => {
            const productCard = document.createElement("div");
            productCard.classList.add("product-card");
            productCard.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <h3>${product.name}</h3>
                <p class="price">R$ ${product.price}</p>
                <p class="category">Categoria: ${product.category}</p>
                <p class="description">${product.description || ""}</p>
                <button class="delete-btn" data-index="${index}">Remover</button>
            `;
            productList.appendChild(productCard);
        });

        document.querySelectorAll(".delete-btn").forEach(button => {
            button.addEventListener("click", (e) => {
                const index = e.target.dataset.index;
                products.splice(index, 1);
                localStorage.setItem("products", JSON.stringify(products));
                renderProducts();
            });
        });
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const name = document.getElementById("product-name").value;
        const price = document.getElementById("product-price").value;
        const image = document.getElementById("product-image").value;
        const category = document.getElementById("product-category").value;
        const description = document.getElementById("product-description").value;

        const newProduct = { name, price, image, category, description };
        products.push(newProduct);
        localStorage.setItem("products", JSON.stringify(products));

        form.reset();
        renderProducts();
    });

    renderProducts();
});
