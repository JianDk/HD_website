$( document ).ready(function(){ 
    //hide all elements
    document.getElementById("localDeliveryForm").style.display = "none";
    document.getElementById("takeawayPickUp").style.display = "none"; 
    $("#localDeliveryCheckoutForm").validate({
        //specifying rules for the validation
        rules: {
            customerName: {required : true},     
        },
        messages: {
            customerName: {required : "Please enter your name"},
        },

        submitHandler: function(form) {
            form.submit();
        }
    })
})

function localDeliveryCheckoutFormValidation() {
    alert("form validation called");
}

document.getElementById("paymentButton").addEventListener("click", function() {
    //Collect all the fields value and send it to the serve

    //collect address
    var addressField = document.getElementById("valgtadresse");
    addressField = addressField.textContent.split(":");
    localDeliveryCheckoutFormValidation();

    console.log(addressField[1].trim());

    $.ajax({
        url : "localDeliveryPayment",
        type : "get",

        success: function(response) {
            
            if (response['paymentIdCreation'] == true) {
                console.log(response);
                const checkoutOptions = {
                    checkoutKey: "test-checkout-key-e1cf229bca36462f887e9d981a7a0313", // Replace!
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
