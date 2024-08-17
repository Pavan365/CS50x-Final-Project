/*
Show the values of the risk-free-rate and sigma sliders on the
options/pricing.html page.
*/
document.addEventListener("DOMContentLoaded", function() {
    let rfrSlider = document.getElementById("rfr");
    let rfrValue = document.getElementById("rfrValue");

    rfrValue.value = rfrSlider.value;
    rfrSlider.oninput = function() {
        rfrValue.value = this.value;
    };

    let sigmaSlider = document.getElementById("sigma");
    let sigmaValue = document.getElementById("sigmaValue");

    sigmaValue.value = sigmaSlider.value;
    sigmaSlider.oninput = function() {
        sigmaValue.value = this.value;
    };
});
