/*
Plot the time-series of a stock when the stock-form on the
options/index.html page is submitted, and data for a stock is
retrieved.
*/
document.addEventListener("DOMContentLoaded", function() {
    plotStockPrices();
});


// Plot the time-series of a stock.
function plotStockPrices() {
    let chartStatus = Chart.getChart("stock-prices");
    if (chartStatus != undefined) {
        chartStatus.destroy();
    }

    new Chart(
        document.getElementById("stock-prices"),
        {
            type: "line",
            data: {
                labels: Object.keys(closingPrices),
                datasets: [
                    {
                        label: "Closing Price",
                        data: Object.values(closingPrices)
                    }
                ]
            }
        }
    );
}
