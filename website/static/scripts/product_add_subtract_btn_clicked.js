function itemQuantityChangeButton(element) {
    $.ajax({
        url: "changeItemQuantityInBasket",
        type: "get",
        data: {
            itemToChange: element.id,
        },
        success: function(response) {
            console.log(response);
            //store the session id in local session
            localStorage.setItem("hd2900TakeAwayCartId", response["sessionid"]);
        }
    })
}