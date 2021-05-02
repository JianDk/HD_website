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
            
                //If updated quantity is 0, then the quantity textfield placeholder should be blank
                if (response["updatedQuantity"] <= 0) {
                    quantityFieldElement.placeholder = "";
                } else {
                    quantityFieldElement.placeholder = response["updatedQuantity"].toString();
                }
                //Store session id to the browser
                localStorage.setItem(response["sessionIdKey"], response["sessionId"]);
            }
        }
    })
}