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
          //Check first which page called this method. 
          var urlSource = window.location.href;
          if (urlSource.endsWith("hd2900_takeaway_webshop") == 1) {
            var deliveryMessageTag = document.getElementById("valgtadresse");
            if (response['distance_within_delivery_range'] == 1) {
              deliveryMessageTag.innerHTML = "<span style='color: green; font-family : hdFont;'>We deliver to this address</span>"
            } else {
              deliveryMessageTag.innerHTML = "<span style='color: red; font-family : hdFont;'>Sorry we don't delivery to this address</span>"
            }
          } else if (urlSource.endsWith("deliveryFormCheckout") ==1) {
            var localDeliveryTag = document.getElementById("localDeliveryForm");
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
        }
      })
    }
  })