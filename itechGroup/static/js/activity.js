$(document).ready(function() {
    $('.rating input').change(function () {
        var radio = $(this);
        $('.rating .selected').removeClass('selected');
        radio.closest('label').addClass('selected');
      });

    $('#submitReview').click(function() {
        var rating = $("#reviewRating input[type='radio']:checked").val()
        var title = $("#reviewTitle").val() || "Review"
        var description = $("#reviewDescription").val()
        
        var path_parts = window.location.pathname.split('/');
        var activity = path_parts[path_parts.length - 2];
    
        if(!rating) {
            alert("Please specifiy a rating.");
        }
        else {
            $.post(postPath, {
                "activity": activity,
                "title": title,
                "rating": rating,
                "description": description,
                "csrfmiddlewaretoken": csrfToken
            },
            function(response, status){
                window.location.reload(true); 
            });
        }
    });
});