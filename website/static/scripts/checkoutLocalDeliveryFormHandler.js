$( document ).ready(function(){ 
    //hide all elements
    document.getElementById("localDeliveryForm").style.display = "none";
    document.getElementById("takeawayPickUp").style.display = "none"; 
})

function localDeliveryFormValidation(event) {

    //Name must only be alphabets including æ,ø,å. No other characters are allowed
    var name = document.getElementById("customerName").value.trim();
    var nametest = /^[a-z,æ,ø,å,A-Z,Æ,Ø, ,]+$/.test(name);
    if (nametest == false) {
        event.preventDefault();
        document.getElementById("errormsg").innerHTML = "Name cannot contain special character or number";
        document.getElementById("errormsg").style.color = "red";
    }

    //Check mobile phone number
    var mobilePhone = document.getElementById("customerMobile").value.trim();
    var mobilePhoneTest = /^\+?[0-9]+/.test(mobilePhone);
    if (mobilePhoneTest == false) {
        event.preventDefault();
        document.getElementById("errormsg").innerHTML = "Mobile phone number must either be in format 12345678 or for international number +4512345678";
        document.getElementById("errormsg").style.color = "red";    
    }
}