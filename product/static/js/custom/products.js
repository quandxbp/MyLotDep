function formatProductName(product_name) {
    $(product_name).each(function() {
        let productName = $(this).text();
        if (productName.length > 55) {
            let reduceProductName = productName.match(/(.{1,52})/g)[0] + "...";
            $(this).text(reduceProductName);
        }
    });
}

$(function() {
    formatProductName('.product-name')
});
