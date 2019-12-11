function formatPrice(price_tag) {
    $(price_tag).each(function() {
        let price = $(this).text();
        if (price.includes(".0000")) {
            price = price.replace(".0000", "");
        }
        let newPrice = price.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.') + " ₫";
        $(this).text(newPrice)
    });
}

$(function() {
    formatPrice('.price');
});