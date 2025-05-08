document.addEventListener("DOMContentLoaded", () => {
    const productList = document.getElementById("product-list");
    const categoryFilter = document.getElementById("category-filter");
    const searchInput = document.getElementById("search-input");
    const clearFilterBtn = document.getElementById("clear-filter");
    const priceFilter = document.getElementById("price-filter");

    function filterProducts() {
        const cards = productList.querySelectorAll(".product-card");
        const searchValue = searchInput.value.toLowerCase();
        const categoryValue = categoryFilter.value;

        cards.forEach(card => {
            const name = card.querySelector("h3").textContent.toLowerCase();
            const category = card.dataset.category.toLowerCase();

            const matchesName = name.includes(searchValue);
            const matchesCategory = categoryValue === "all" || category === categoryValue;

            card.style.display = (matchesName && matchesCategory) ? "flex" : "none";
        });
    }
    clearFilterBtn.addEventListener("click", () => {
        searchInput.value = "";
        categoryFilter.value = "all";
        priceFilter.value = "default";
        filterProducts();
    });

    categoryFilter.addEventListener("change", filterProducts);
    searchInput.addEventListener("input", filterProducts);
    priceFilter.addEventListener("change", () => {
        const cards = Array.from(productList.querySelectorAll(".product-card"));

        const getPrice = card => parseFloat(
            card.querySelector(".price").textContent
                .replace("R$", "")
                .replace(".", "")
                .replace(",", ".")
        );

        if (priceFilter.value === "low-to-high") {
            cards.sort((a, b) => getPrice(a) - getPrice(b));
        } else if (priceFilter.value === "high-to-low") {
            cards.sort((a, b) => getPrice(b) - getPrice(a));
        }

        productList.innerHTML = "";
        cards.forEach(card => productList.appendChild(card));
    });

    filterProducts();
});