function select_config(itemId) {
    $.ajax({
        type: 'POST',
        url: '/config/select/' + itemId,
        success: function(response) {
            window.location.reload();
        }
    });
}

function remove_config(itemId) {
    $.ajax({
        type: 'POST',
        url: '/config/remove/' + itemId,
        success: function(response) {
            window.location.reload();
        },
    });
}
