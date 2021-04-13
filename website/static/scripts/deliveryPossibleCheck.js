// JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

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
    input_address = {"deliveryAddress" : input_address};

    //At this point it is certain that the address is not empty and call server can be made for distance check
    const xmlhttprequest = new XMLHttpRequest();

    xmlhttprequest.onload = function () {
        alert("something received by server response");
    };

    xmlhttprequest.open("POST", "check-address-for-deliverable");

    xmlhttprequest.setRequestHeader('Content-Type', 'application/json');
    xmlhttprequest.setRequestHeader("X-CSRFToken", csrftoken);

    xmlhttprequest.send(JSON.stringify(input_address));
});



