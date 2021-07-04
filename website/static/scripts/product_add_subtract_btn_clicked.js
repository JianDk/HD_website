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
                if (response["updatedQuantity"] <= 0) {
                    quantityFieldElement.placeholder = "0";
                    //If in delivery pickup page before the checkout, item total price field will be set to 0 kr as well
                    var itemTotalPriceElement = document.getElementById("totalPrice_" + response["product_to_update_slug"]);
                    if (itemTotalPriceElement != null) {
                        itemTotalPriceElement.innerHTML = "0 kr";
                    }
                } else {
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
                //Update the table with product item list
                response["ordered_product_items_list"].forEach(function (item) {
                    var itemTotalPriceId = document.getElementById("totalPrice_" + item['productSlug']);
                    itemTotalPriceId.innerHTML = item['totalPrice_for_ordered_item'] + " kr"

                    console.log(item);
                })

                //Update the total price
                var totalPriceElement = document.getElementById("totalPrice");
                totalPriceElement.innerHTML = "Total : " + response["totalPrice"] + ' kr';

                //Check if total price is above the minimum limit for delivery. If true, then the button is made active
                var deliveryButton = document.getElementById("localDeliveryButton");
                var deliveryPossibleElement = document.getElementById("deliveryPossibleMessage");
                if (deliveryButton !== null) {
                    if (response["deliveryButtonActive"] == 1) {
                        deliveryButton.disabled= false;
                        deliveryPossibleElement.innerHTML = "";                    
                    } else {
                        deliveryButton.disabled = true;
                        deliveryPossibleElement.innerHTML = "Minimum order for takeaway delivery : " + response["minimum_totalPrice_for_delivery"] + ' kr';
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