
$('#Logout').click(function () {
    $.ajax({
        url: "operatorbutton",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            localStorage.clear();
            window.location.href = "/logout/";
        }
    });
});