$(function() {
    let searchInput = $("#search-field input");
    $(searchInput).keyup(function (e) {
        let searchText = $(this).val();
        if (searchText.length > 3) {
            $.ajax({
                url: './api/v1/search_product',
                type: "GET",
                data: {
                    'search_data': searchText,
                },
                success: function (result) {
                    let products = result['products'];
                    if (products.length !== 0) {
                        let searchView = '';
                        products.forEach(function (product, index) {
                            searchView += addNewSearchRecordView(product);
                        });
                        $('#suggestion-items').html(searchView);
                        formatPrice('.nav-price');
                        $('#suggestion-box').show();
                    }
                },
                error: function (error) {
                    console.log(error);
                }
            })
        } else {
            $('#suggestion-box').hide();
        }
    });

    function addNewSearchRecordView(product) {
        let platform_thumb = false;
        if (product.platform === 'tiki') {
            platform_thumb = '/static/images/tiki.png';
        }
        else if (product.platform === 'adayroi') {
            platform_thumb = '/static/images/adayroi.png';
        }

        return `<a class="suggestion-item row">
                        <div class="col-md-3 nav-thumb">
                            <img src="` + product.thumb_url+ `" height="100" width="100" />
                        </div>
                        <div class="col-md-7 nav-product-info">
                            <h6 class="nav-product-name">` + product.product_name + `</h6>
                            <p class="nav-product-price nav-price red-color">` + product.sale_price + `</p>
                            <p class="font-14">
                                <span class="nav-product-price-stock muted-price nav-price">` + product.list_price + `</span>
                                <span class="nav-product-discount">-` + product.discount_rate + `%</span>
                            </p>
                        </div>
                        <div class="col-md-2 nav-platform text-center">
                            <img src="` + platform_thumb + `" height="50" width="50" />
                        </div>
                    </a>`;

    }

    // $(searchInput).keyup(delay(function (e) {
    //     let searchText = $(this).val();
    //     if (searchText.length > 3) {
    //         $.ajax({
    //             url: './api/v1/search_product',
    //             type: "GET",
    //             data: {
    //                 'search_data': searchText,
    //             },
    //             success: function (result) {
    //                 console.log(result);
    //             },
    //             error: function (error) {
    //                 console.log(error);
    //             }
    //         })
    //     }
    // },3000));
});