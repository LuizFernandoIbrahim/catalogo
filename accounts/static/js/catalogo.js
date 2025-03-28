document.addEventListener("DOMContentLoaded", () => {
    const productList = document.getElementById("product-list");
    const categoryFilter = document.getElementById("category-filter");
    const searchInput = document.getElementById("search-input");
    const clearFilterBtn = document.getElementById("clear-filter");

    let products = JSON.parse(localStorage.getItem("products")) || [];

    function renderProducts(filteredProducts = products) {
        productList.innerHTML = "";

        if (filteredProducts.length === 0) {
            productList.innerHTML = "<p>Nenhum produto encontrado.</p>";
        } else {
            filteredProducts.forEach((product, index) => {
                productList.innerHTML += `
                    <div class="product-card">
                        <img src="${product.image}" alt="${product.name}">
                        <h3>${product.name}</h3>
                        <p class="price">R$ ${product.price}</p>
                        <p class="category">Categoria: ${product.category}</p>
                        <p class="description">${product.description || "Sem descrição disponível."}</p>
                        <button class="details-btn" data-index="${index}">Ver Detalhes</button>
                    </div>
                `;
            });

            // Adiciona os eventos para os botões "Ver Detalhes"
            const detailButtons = document.querySelectorAll(".details-btn");
            detailButtons.forEach(button => {
                button.addEventListener("click", (e) => {
                    const index = e.target.dataset.index;
                    const selectedProduct = filteredProducts[index];
                    localStorage.setItem("selectedProduct", JSON.stringify(selectedProduct));
                    window.location.href = "/detalhes/";
                });
            });
        }
    }

    function loadCategories() {
        const categories = [...new Set(products.map(p => p.category))];
        categoryFilter.innerHTML = `<option value="all">Todas as Categorias</option>`;
        categories.forEach(category => {
            categoryFilter.innerHTML += `<option value="${category}">${category}</option>`;
        });
    }

    function filterProducts() {
        let filtered = products;

        if (categoryFilter.value !== "all") {
            filtered = filtered.filter(product => product.category === categoryFilter.value);
        }

        if (searchInput.value.trim() !== "") {
            filtered = filtered.filter(product =>
                product.name.toLowerCase().includes(searchInput.value.toLowerCase())
            );
        }

        renderProducts(filtered);
    }

    categoryFilter.addEventListener("change", filterProducts);
    searchInput.addEventListener("input", filterProducts);
    clearFilterBtn.addEventListener("click", () => {
        searchInput.value = "";
        categoryFilter.value = "all";
        renderProducts();
    });

    renderProducts();
    loadCategories();
});