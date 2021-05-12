function itemQuantityChangeButton(element) {
    $.ajax({
        url: "changeItemQuantityInBasket",
        type: "get",
        data: {
            itemToChange: element.id,
        },
        success: function(response) {
            if (response["update_field"] == 1) {
                //Update the product quantity to the text field
                var quantityFieldElement = document.getElementById("text_" + response["product_to_update_slug"]);
                var shoppingCartElement = document.getElementById("lblCartCount");

                //If updated quantity is 0, then the quantity textfield placeholder should be blank
                if (response["updatedQuantity"] <= 0) {
                    quantityFieldElement.placeholder = "";
                    if (shoppingCartElement) {
                        shoppingCartElement.innerHTML = response["totalItemsInBasket"];
                    }
                } else {
                    quantityFieldElement.placeholder = response["updatedQuantity"].toString();
                    if (shoppingCartElement) {
                        shoppingCartElement.innerHTML = response["totalItemsInBasket"];
                    }
                }
                //Store session id to the browser
                localStorage.setItem(response["sessionIdKey"], response["sessionId"]);
            }
        }
    })
}

function checkoutPlusMinusPressed(element) {
    itemQuantityChangeButton(element);
    //Get the total price and manage the part of the logics that determines if delivery is possible
    $.ajax({
        url: "isPriceAboveDeliveryLimit",
        type: "get",
        success: function(response){
            //check if for some reasons, e.g. session has expired, product no longer available...etc, then the checkout page will be updated
            if (response["pageRefresh"] == true) {
                alert("session is outdated, you will be sent back");
                window.location.href = "/takeawayCheckout";
            } else {
                //Update the total price
                var totalPriceElement = document.getElementById("totalPrice");
                console.log(response);
                totalPriceElement.innerHTML = response["totalPrice"];
            }
        }
    })
}