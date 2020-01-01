function formatPriceValue(price) {
    return price.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.') + " ₫";
}

$(document).ready(function () {
    let spid = $("#data-spid").data('spid');
    let product_id = $("#data-product-id").data('product-id');
    let platform = $("#data-platform").data('platform');
    let lowest_price_spid = $("#data-lowest-price-spid").data('lowest-price-spid');
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
        complete: function () {
            $(".loading").hide();
        }
    });
    // End Forecasting

    // Current Price statistics
    $.ajax({
        url: "/api/v1/get_current_product_price",
        data: {
            "spid": spid,
            "lowest_price_spid": lowest_price_spid,
            "product_id": product_id,
            "platform": platform
        },
        method: "GET",
        success: function (result) {
            let currentPriceInfo = result['current_price_info'];
            let lowestPriceInfo = result['lowest_price_info'];

            let curSalePrice = currentPriceInfo['sale_price'];
            let curDateTime = currentPriceInfo['cur_datetime'];

            let lowestSalePrice = lowestPriceInfo['sale_price'];
            let lowestDateTime = lowestPriceInfo['cur_datetime'];

            $("#cur_sale_price").text(formatPriceValue(curSalePrice));
            $("#cur_datetime").text(curDateTime);

            $("#lowest_sale_price").text(formatPriceValue(lowestSalePrice));
            $("#lowest_datetime").text(lowestDateTime);
        },
        error: function (err) {
            console.log("Error: " + err.statusText);
        },
        complete: function () {
        }
    });
    // \ Current Price statistics

    // Current Special Price statistics
    $.ajax({
        url: "mongo/api/v1/get_special_price_current_product",
        data: {
            "spid": spid,
            "lowest_price_spid": lowest_price_spid
        },
        method: "GET",
        success: function (result) {
            // Highest product
            let currentPriceData = result['cur_special_price_info'];

            let curHighestDateTime = currentPriceData['highest'][0];
            let curHighestSalePrice = currentPriceData['highest'][1];

            let curLowestDateTime = currentPriceData['lowest'][0];
            let curLowestSalePrice = currentPriceData['lowest'][1];

            let curAverage = currentPriceData['average'];
            let curPeriod = currentPriceData['period'];

            $("#cur_highest_sale_price").text(formatPriceValue(curHighestSalePrice));
            $("#cur_highest_datetime").text(curHighestDateTime);

            $("#cur_lowest_sale_price").text(formatPriceValue(curLowestSalePrice));
            $("#cur_lowest_datetime").text(curLowestDateTime);

            $("#cur_average").text(formatPriceValue(curAverage));

            $('.cur_period').each(function (index) {
                $(this).text(curPeriod);
            });

            // Lowest product
            let lowestPriceData = result['lowest_special_price_info'];

            let lowestHighestDateTime = lowestPriceData['highest'][0];
            let lowestHighestSalePrice = lowestPriceData['highest'][1];

            let lowestLowestDateTime = lowestPriceData['lowest'][0];
            let lowestLowestSalePrice = lowestPriceData['lowest'][1];

            let lowestAverage = lowestPriceData['average'];
            let lowestPeriod = lowestPriceData['period'];

            $("#lowest_highest_sale_price").text(formatPriceValue(lowestHighestSalePrice));
            $("#lowest_highest_datetime").text(lowestHighestDateTime);

            $("#lowest_lowest_sale_price").text(formatPriceValue(lowestLowestSalePrice));
            $("#lowest_lowest_datetime").text(lowestLowestDateTime);

            $("#lowest_average").text(formatPriceValue(lowestAverage));

            $('.lowest_period').each(function (index) {
                $(this).text(lowestPeriod);
            });
        },
        error: function (err) {
            console.log("Error: " + err.statusText);
        },
        complete: function () {
        }
    });
    // \ Current Special Price statistics
});
