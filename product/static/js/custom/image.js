function resize_image(image_tags){
    $(image_tags).each(function() {
        $(this).css("width", "200px");
        $(this).css("height", "200px");
    });
}

$(function() {
    resize_image('#product-list .thumbnail');
});