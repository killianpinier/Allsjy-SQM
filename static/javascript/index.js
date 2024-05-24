$(document).ready(

    $("#runBtn").click(function() {
        setTimeout(function() {
            location.reload();
        }, 1000);

        $.ajax({
            type: 'POST',
            url: '/run',
            success: function(response) {
                if (response.message != "") {
                    alert(response.message);
                } else {
                    location.reload();
                }
            }   
        });
    }),

    $("#stopBtn").click(function() {
        $.ajax({
            type: 'POST',
            url: '/stop',
            success: function(response) {
                if (response.message != "") {
                    alert(response.message);
                } else {
                    location.reload();
                }
            }
        });
    }),
);