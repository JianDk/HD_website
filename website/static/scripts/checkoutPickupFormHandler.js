function localPickupFormValidation(event) {

    //Name must only be alphabets including æ,ø,å. No other characters are allowed
    var name = document.getElementById("customerName").value.trim();
    var nametest = /^[a-z,æ,ø,å,A-Z,Æ,Ø, ,]+$/.test(name);
    if (nametest == false) {
        event.preventDefault();
        document.getElementById("errormsg").innerHTML = "Name cannot contain special character or number";
        document.getElementById("errormsg").style.color = "red";
    }
}