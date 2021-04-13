var button_check_delivery_possible = document.getElementById("addressSubmitButton");
button_check_delivery_possible.addEventListener("click", function(event){
    //prevent default behavior which is to call django post
    event.preventDefault();
    //Extract user address
    var input_address = document.getElementById("id_address");
    input_address = input_address.value; 
    input_address = input_address.trim();
    //Check if field is empty
    if (input_address == "") {
        return false;
    }
    //At this point it is certain that the address is not empty and call server can be made for distance check

    alert(input_address);
});

// $(document).ready(function () {
//     $("#buttonCheckDeliveryPossible").submit(function (event) {
//         event.preventDefault();
//         alert("hello world");
//     })
//     });

