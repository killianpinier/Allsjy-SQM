$(document).ready(

    $("#runBtn").click(function() {
        $.ajax({
            type: 'POST',
            url: '/run',
            success: function(response) {
                alert(response);
            }
        });
    }),
);