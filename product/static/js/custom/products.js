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
    formatProductName('.product-name');

    // initialize tooltip
    $(document).ready(function(){
      $('[data-toggle="tooltip"]').tooltip();
    });

    // Expand description content
    $("#product-description #description-expand-btn").on("click", function () {
        $("#product-description #description-content").css({
            'max-height': 'none',
            'overflow': 'none',
        });

        $(this).hide();
        $("#product-description #description-reduce-btn").show();
    });

    //Reduce
    $("#product-description #description-reduce-btn").on("click", function () {
        $("#product-description #description-content").css({
            'max-height': '600px',
            'overflow': 'hidden',
        });

        $(document).scrollTop($("#product-description").offset().top);

        $(this).hide();
        $("#product-description #description-expand-btn").show();
    });

    // Remove redundant Text
    $("#product-description #description-content").contents().filter(function(){
        return (this.nodeType == 3);
    }).remove();
    $("#product-description #description-content br").remove();
});
