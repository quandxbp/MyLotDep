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

$(function() {
      $(".regular").slick({
        dots: true,
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 3
      });
      $(".center").slick({
        dots: true,
        infinite: true,
        centerMode: true,
        slidesToShow: 3,
        slidesToScroll: 3
      });
      $(".variable").slick({
        dots: true,
        infinite: true,
        variableWidth: true
      });
});