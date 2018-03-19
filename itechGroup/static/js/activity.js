$(document).ready(function() {
    $('.rating input').change(function () {
        var radio = $(this);
        $('.rating .selected').removeClass('selected');
        radio.closest('label').addClass('selected');
      });

    $('#submitReview').click(function() {
        var rating = $("#reviewRating input[type='radio']:checked").val()
        var title = $("#reviewTitle").val()
        var description = $("#reviewDescription").val()

        if(!rating) {
            alert("Please specifiy a rating.");
        }
        else {
            // send to server

            $("#reviewModal").modal('hide');
            $('#addReviewBtn').hide();
        }
    });
});