var autocomplete;

// Function to autocomplete Google Maps query, code based off GoogleMapsAPI documentation
function initAutocomplete() {
    // Create the autocomplete object, restricting the search to geographical
    // location types.
    autocomplete = new google.maps.places.Autocomplete(
                    /** @type {!HTMLInputElement} */(document.getElementById('id_address')),
        { types: ['geocode'] });

    // When the user selects an address from the dropdown, populate the address
    // fields in the form.
    autocomplete.addListener('place_changed', fillInAddress);
}

// Function to fill the hidden address fields that go into the database once 
// address is autocompleted.
function fillInAddress() {
    // Retrieve place
    var place = autocomplete.getPlace();

    // Show map to user
    frame_maps = document.getElementById("iframemaps");
    frame_maps.setAttribute("src", "https://www.google.com/maps/embed/v1/place?key=" + GOOGLE_MAPS_KEY +"&q=" + place.formatted_address);
    frame_maps.removeAttribute("hidden");

    // Fill hidden fields
    $("#act-lat").val(place.geometry.location.lat());
    $("#act-lng").val(place.geometry.location.lng());
}

// Function to fill the hidden tags input that goes into the database
function fillTagsInput(taggle){
    var tags = taggle.getTagValues().toString();
    $("#tags-string").val(tags);
}

// Function to start up Taggle on tags input field
$(document).ready(function() {
    t = new Taggle('tags-field', {
        onTagAdd: function(event, tag) { fillTagsInput(t) },
        onTagRemove: function(event, tag) { fillTagsInput(t) }
    });

    $("span.taggle_placeholder").hide();
});