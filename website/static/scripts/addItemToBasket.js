function addItemBtnClicked(element) {
    $.ajax({
        url: "addItemToBasket",
        type: "get",
        data: {
            itemToAdd: element.id,
        },
        success: function(response) {
            console.log(response);
            //store the session id in local session
            localStorage.setItem("hd2900TakeAwayCartId", response["sessionid"]);
        }
    })
}