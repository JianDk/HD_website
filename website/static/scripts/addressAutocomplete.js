"use strict"

dawaAutocomplete.dawaAutocomplete( document.getElementById("checkoutLocalDeliveryAddress"), {
  select: function(selected) {
      document.getElementById("valgtadresse").innerHTML= selected.tekst;
      //check if address is deliverable
      $.ajax({
        url: "local_delivery_checkout_is_address_deliverable",
        type: "get",
        data: {x : selected.data.x,
              y: selected.data.y},
        success: function(response) {
          var localDeliveryTag = document.getElementById("localDeliveryForm");
          console.log(localDeliveryTag);
          if (response['distance_within_delivery_range'] == 1) {
            localDeliveryTag.style.display = "block";
            document.getElementById("takeawayPickUp").style.display = "none"; 
            document.getElementById("valgtadresse").innerHTML = "Takeaway can be delivered to " + selected.tekst
          } else {
            localDeliveryTag.style.display = "none";
            document.getElementById("takeawayPickUp").style.display = "block"; 
            document.getElementById("valgtadresse").innerHTML = "Sorry your address " + selected.tekst + " is outside our delivery range. Takeaway is available for pickup."
          }
        }
      })
  }
});