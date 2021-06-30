$(document).ready(function() {
    //Get payment id from server
    var paymentId = document.getElementById("paymentId").innerHTML.trim();
    var checkoutKey = document.getElementById("checkoutKey").innerHTML.trim();

    const checkoutOptions = {
        checkoutKey: checkoutKey,
        paymentId: paymentId,
        containerId: "checkout-container-div",
        };
        
        const checkout = new Dibs.Checkout(checkoutOptions)
        checkout.on('payment-completed', function (response) {
            window.location = '/paymentComplete';
        });
});
            
