function formatPriceValue(price) {
    return price.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.') + " ₫";
}