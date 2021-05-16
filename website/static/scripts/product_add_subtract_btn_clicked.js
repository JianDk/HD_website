// function itemQuantityChangeButton(element) {
//     $.ajax({
//         url: "changeItemQuantityInBasket",
//         type: "get",
//         data: {
//             itemToChange: element.id,
//         },
//         success: function(response) {
//             if (response["update_field"] == 1) {
//                 //Update the product quantity to the text field
//                 var quantityFieldElement = document.getElementById("text_" + response["product_to_update_slug"]);
//                 var shoppingCartElement = document.getElementById("lblCartCount");

//                 //If updated quantity is 0, then the quantity textfield placeholder should be blank
//                 if (response["updatedQuantity"] <= 0) {
//                     quantityFieldElement.placeholder = "";
//                     if (shoppingCartElement) {
//                         shoppingCartElement.innerHTML = response["totalItemsInBasket"];
//                     }
//                 } else {
//                     quantityFieldElement.placeholder = response["updatedQuantity"].toString();
//                     if (shoppingCartElement) {
//                         shoppingCartElement.innerHTML = response["totalItemsInBasket"];
//                     }
//                 }
//                 //Store session id to the browser
//                 localStorage.setItem(response["sessionIdKey"], response["sessionId"]);
//             }
//         }
//     })
//     console.log("first function complete");
// }


function itemQuantityChanged(element) {
    return new Promise((resolve, reject) => {

        $.ajax({
            url: "changeItemQuantityInBasket",
            type: "get",
            data: {itemToChange: element.id},

        success : function(response) {
            if (response["update_field"] == 1) {
                    
                //Update the product quantity to the text field
                var quantityFieldElement = document.getElementById("text_" + response["product_to_update_slug"]);
                var shoppingCartElement = document.getElementById("lblCartCount");
                
                //If updated quantity is 0, then the quantity textfield placeholder should be blank
                if (response["updatedQuantity"] <= 0) {quantityFieldElement.placeholder = "";} else {
                    quantityFieldElement.placeholder = response["updatedQuantity"].toString();
                }

                if (shoppingCartElement) {shoppingCartElement.innerHTML = response["totalItemsInBasket"];}
            }
            
            //Store session id to the browser
            localStorage.setItem(response["sessionIdKey"], response["sessionId"]);
            resolve()
        },
        
        error : function() {
            reject()
        },
    })})}
        

function itemQuantityChangeButton(element) {
    let promise = itemQuantityChanged(element)
}

function updateTotalPrice(){
    //Get the total price and manage the part of the logics that determines if delivery is possible
    $.ajax({
        url: "isPriceAboveDeliveryLimit",
        type: "get",
        success: function(response){
            //check if for some reasons, e.g. session has expired, product no longer available...etc, then the checkout page will be updated
            if (response["pageRefresh"] == true) {
                window.location.href = "/takeawayCheckout";
            } else {
                //Update the total price
                var totalPriceElement = document.getElementById("totalPrice");
                totalPriceElement.innerHTML = "Total : " + response["totalPrice"] + ' kr';

                //Check if total price is above the minimum limit for delivery. If true, then the button is made active
                var deliveryButton = document.getElementById("localDeliveryButton");
                if (deliveryButton !== null) {
                    console.log("here we are");
                    console.log(response["deliveryPossible"]);
                    if (response["deliveryPossible"] == 1) {
                        deliveryButton.disabled= false;
                    } else {
                        deliveryButton.disabled = true;
                    }
                }
            }
        }
    })
}

function checkoutPlusMinusPressed(element) {
    let promise = itemQuantityChanged(element)
    promise.then(updateTotalPrice);
    promise.catch(function(){window.location.href = "/takeawayCheckout";});
    
}