$('#id_id_window').mouseenter(function () {
    $.ajax({
        url: "windowbutton",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            $('#id_id_window option').remove();
            for (var i = 0; i < response.windows_l.length; i++) {
                $('#id_id_window').prepend('<option value="'+ (i+1) +'">' + response.windows_l[i] + '</option>');
            }
        }
    });
});

$(function () {
    $.ajax({
        url: "windowbutton",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            localStorage.clear();
            $('#id_id_window option').remove();
            for (var i = 0; i < response.windows_l.length; i++) {
                $('#id_id_window').prepend('<option value="' + (i + 1) + '">' + response.windows_l[i] + '</option>');
            }
        }
    });
});

$('#Enter').click(function () {
    $.ajax({
        url: "windowbutton",
        method: 'POST',
        data: {
            name: $('select option:selected').text(),
            click: true
        },
        success: function (response) {
            window.location.href = "./operator/"
        }
    });
});