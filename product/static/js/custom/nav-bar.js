$(function() {
    let searchInput = $("#search-field input");
    $(searchInput).keyup(function (e) {
        let searchTerm = $(this).val();
        if (searchTerm.length > 3) {
            $.ajax({
                url: './api/v1/search_product',
                type: "GET",
                data: {
                    'q': searchTerm,
                },
                success: function (result) {
                    console.log(result);
                    let product_templates = result['product_templates'];
                    let products = result['products'];
                    let platforms = result['platforms'];
                    let searchView = '';
                    if (product_templates.length !== 0) {
                        product_templates.forEach(function (product, index) {
                            searchView += addNewProductTemplate(product);
                        });
                    }
                    if (platforms.length !== 0) {
                        platforms.forEach(function (platform, index) {
                            let platformName = platform[0];
                            let platformCount = platform[1];
                            searchView += addNewPlatform(platformName, platformCount, searchTerm);
                        });
                    }
                    if (products.length !== 0) {
                        products.forEach(function (product, index) {
                            searchView += addNewSearchRecordView(product);
                        });
                    }
                    $('#suggestion-items').html(searchView);
                    formatPrice('.nav-price');
                    $('#suggestion-box').show();
                    // let producstData = result['product_data'];
                    // if (producstData.length !== 0 ) {
                    //     let searchView = '';
                    //     producstData.forEach(function (productInfo, index) {
                    //         let products = productInfo[0];
                    //         let productCount = productInfo[1];
                    //         products.forEach(function (product, index) {
                    //             searchView += addNewSearchRecordView(product);
                    //         });
                    //
                    //         if (productCount > 0) {
                    //             searchView += addNewProductCount(productCount, searchTerm);
                    //         }
                    //     });
                    //     $('#suggestion-items').html(searchView);
                    //     formatPrice('.nav-price');
                    //     $('#suggestion-box').show();
                    // }
                },
                error: function (error) {
                    console.log(error);
                }
            })
        } else {
            $('#suggestion-box').hide();
        }
    });

    function addNewProductTemplate(product) {
        return `<a href="/san-pham?q=` + product + `" class="suggestion-item row cust-border-bottom">
            <div class="col-md-12 ">
                <span class="p-3">` + product + `</span>
            </div>
        </a>`
    }

    function addNewSearchRecordView(product) {
        let platform_thumb = false;
        if (product.platform === 'tiki') {
            platform_thumb = '/static/images/tiki.png';
        }
        else if (product.platform === 'adayroi') {
            platform_thumb = '/static/images/adayroi.png';
        }

        return `<a class="suggestion-item row cust-border-bottom">
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

    function addNewPlatform(platform, productCount, searchTerm) {
        return `<a href="/san-pham?q=` + searchTerm + `&platform=` + platform + `" 
                class="suggestion-item row cust-border-bottom">
            <div class="col-md-12 ">
                <span class="p-3">Xem 
                    <span class="blue-color">` + productCount + ` </span>
                     sản phẩm liên quan với 
                     <strong class="font-weight-bold">` + searchTerm + ` </strong> 
                     ở 
                    <span class="blue-color">`+ platform +` </span>
                </span>
            </div>
        </a>`
    }

    function addNewProductCount(productCount, searchTerm) {
        return `<div class="row text-center m-1">
            <div class="col-md-12">
                <a href="/san-pham?q=` + searchTerm + `"><i class="fa fa-plus-circle blue-color"></i> &nbsp;Xem thêm <span class="blue-color">` + productCount + `</span> sản phẩm cùng loại</a>
            </div>
        </div>`
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