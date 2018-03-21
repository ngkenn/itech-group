$(document).ready(function() {
    // Function to handle showing the selected amount of stars on a review
    $('.rating input').change(function () {
        var radio = $(this);
        $('.rating .selected').removeClass('selected');
        radio.closest('label').addClass('selected');
      });

    // Function that makes AJAX call to submit a review
    $('#submitReview').click(function() {
        // Gathering data
        var rating = $("#reviewRating input[type='radio']:checked").val()
        var title = $("#reviewTitle").val() || "Review"
        var description = $("#reviewDescription").val()
        
        var path_parts = window.location.pathname.split('/');
        var activity = path_parts[path_parts.length - 2];
    
        if(!rating) {   // Validation: not continuing if it doesn't include a rating
            alert("Please specifiy a rating.");
        }
        else {  // Make POST request
            $.post(postPath, {
                "activity": activity,
                "title": title,
                "rating": rating,
                "description": description,
                "csrfmiddlewaretoken": csrfToken
            },
            function(response, status){ // Reload on success
                window.location.reload(true); 
            });
        }
    });
});