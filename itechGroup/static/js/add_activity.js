var autocomplete;

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

function fillInAddress() {
    // Get the place details from the autocomplete object.
    var place = autocomplete.getPlace();
    frame_maps = document.getElementById("iframemaps");
    frame_maps.setAttribute("src", "https://www.google.com/maps/embed/v1/place?key=" + GOOGLE_MAPS_KEY +"&q=" + place.formatted_address);
    frame_maps.removeAttribute("hidden");
}

function fillTagsInput(taggle){
    var tags = taggle.getTagValues().toString();
    $("#tags-string").val(tags);
}

$(document).ready(function() {
    t = new Taggle('tags-field', {
        onTagAdd: function(event, tag) { fillTagsInput(t) },
        onTagRemove: function(event, tag) { fillTagsInput(t) }
    });

    $("span.taggle_placeholder").hide();
});