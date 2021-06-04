$( document ).ready(function(){ 
    //hide all elements
    document.getElementById("localDeliveryForm").style.display = "none";
    document.getElementById("takeawayPickUp").style.display = "none"; 
})

document.getElementById("paymentButton").addEventListener("click", function() {
    //Collect all the fields value and send it to the serve
    $.ajax({
        url : "localDeliveryPayment",
        type : "get",

        success: function(response) {
            
            if (response['paymentIdCreation'] == true) {
                console.log(response);
                const checkoutOptions = {
                    checkoutKey: response['checkoutKey'], // Replace!
                    paymentId: response['paymentId'],
                    containerId: "checkout-container-div",
                  };
                  const checkout = new Dibs.Checkout(checkoutOptions);
                  checkout.on('payment-completed', function (response) {
                    window.location = 'completed.html';
                  });
                }
            }
        })
    })
