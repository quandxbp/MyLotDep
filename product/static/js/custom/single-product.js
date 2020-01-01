function formatPriceValue(price) {
    return price.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.') + " ₫";
}

$(document).ready(function() {
    let spid = $("#data-spid").data('spid');
    let product_id = $("#data-product-id").data('product-id');
    let platform = $("#data-platform").data('platform');
    // Forecasting
    $.ajax({
        url: "/forecast/prophet",
        data: {"spid": spid},
        method: "POST",
        success: function (result) {
            let data = JSON.parse(result);
            let labels = data['labels'];
            let prices = data['prices'];
            if (prices.length === 0) {
                $("#forecast-data").append("<tr><td colspan='2'><p>Dữ liệu không đủ để dự đoán cho sản phẩm này</p></td></tr>");
            } else {
                let price_forecast_html = "";
                for (let i = 0; i < prices.length; i++) {
                    let price = formatPriceValue(prices[i]);
                    price_forecast_html += `
                    <tr>
                        <td class="date-time">` + labels[i] + `</td>
                        <td class="forecast-price red-color">` + price + `</td>
                    </tr>
                `;
                }
                formatPrice(".forecast-price");
                $("#forecast-data").append(price_forecast_html);
            }
        },
        error: function (err) {
            console.log("Error: " + err.statusText);
            $("#forecast-data").append("<tr><td colspan='2'><p>Dữ liệu không đủ để dự đoán cho sản phẩm này</p></td></tr>");
        },
        complete:function () {
            $(".loading").hide();
        }
    });
    // End Forecasting

    // Current Price statistics
    $.ajax({
        url: "/api/v1/get_current_product_price",
        data: {
            "spid": spid,
            "product_id": product_id,
            "platform": platform
        },
        method: "POST",
        success: function (result) {
            let curSalePrice = result['sale_price'];
            let curDateTime = result['cur_datetime'];

            $("#cur_sale_price").text(formatPriceValue(curSalePrice));
            $("#cur_datetime").text(curDateTime);
        },
        error: function (err) {
            console.log("Error: " + err.statusText);
        },
        complete:function () {
        }
    });
    // \ Current Price statistics

    // Current Special Price statistics
    $.ajax({
        url: "mongo/api/v1/get_special_price_current_product",
        data: {
            "spid": spid,
        },
        method: "GET",
        success: function (result) {
            console.log(result);
            // let curSalePrice = result['sale_price'];
            // let curDateTime = result['cur_datetime'];
            //
            // $("#cur_sale_price").text(formatPriceValue(curSalePrice));
            // $("#cur_datetime").text(curDateTime);
        },
        error: function (err) {
            console.log("Error: " + err.statusText);
        },
        complete:function () {
        }
    });
    // \ Current Special Price statistics
});
