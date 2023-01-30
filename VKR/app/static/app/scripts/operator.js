$('#Next').click(function () {
    $.ajax({
        url: "nextbutton",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            if (typeof response.ticket === "undefined")
                location.reload()
            else
                $('#ta').text(response.ticket);
                $('#tb').text(response.service);
                localStorage.setItem('ticket', response.ticket);
                localStorage.setItem('service', response.service);
                localStorage.setItem('hour', response.hour);
                localStorage.setItem('minute', response.minute);
                localStorage.setItem('second', response.second);
        }
    });
});

$('#Cancel').click(function () {
    $.ajax({
        url: "cancelbutton",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            if (typeof response.ticket === "undefined")
                location.reload()
            else
                $('#ta').text(response.ticket);
                $('#tb').text(response.service);
                localStorage.setItem('ticket', response.ticket);
                localStorage.setItem('service', response.service);
                localStorage.setItem('hour', response.hour);
                localStorage.setItem('minute', response.minute);
                localStorage.setItem('second', response.second);
        }
    });
});

$('#Delay').click(function () {
    if (!$('#Delay').hasClass('return')) {
        $.ajax({
            url: "delaybutton",
            method: 'POST',
            data: {
                click: true
            },
            success: function (response) {
                if (typeof response.ticket === "undefined")
                    location.reload()
                else
                    $('#Delay').addClass('return')
                    $('#Delay').attr("value", "Вернуть талон " + response.ticket_r);
                    $('#ta').text(response.ticket);
                    $('#tb').text(response.service);
                    localStorage.setItem('ticket_r', response.ticket_r);
                    localStorage.setItem('ticket', response.ticket);
                    localStorage.setItem('service', response.service);
                    localStorage.setItem('hour', response.hour);
                    localStorage.setItem('minute', response.minute);
                    localStorage.setItem('second', response.second);
            }
        });
    }
    else {
        $.ajax({
            url: "returnbutton",
            method: 'POST',
            data: {
                click: true
            },
            success: function (response) {
                if (typeof response.ticket === "undefined")
                    location.reload()
                else
                    $('#Delay').removeClass('return')
                    $('#Delay').attr("value", "Отложить");
                    $('#ta').text(response.ticket);
                    $('#tb').text(response.service);
                    localStorage.removeItem('ticket_r');
                    localStorage.setItem('ticket', response.ticket);
                    localStorage.setItem('service', response.service);
                    localStorage.setItem('hour', response.hour);
                    localStorage.setItem('minute', response.minute);
                    localStorage.setItem('second', response.second);
            }
        });
    }
});

$('#Redirect').click(function () {
    $.ajax({
        url: "redirectbutton",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            if (typeof response.windows_l === "undefined")
                location.reload()
            else
                $('#myModal').css('display', 'flex');
                $('#id_id_window option').remove();
            if (response.windows_l.length != 0) {
                $('#Red').removeAttr('disabled');
                for (var i = 0; i < response.windows_l.length; i++) {
                    $('#id_id_window').prepend('<option value="' + (i + 1) + '">' + response.windows_l[i] + '</option>');
                }
            }
            else $('#Red').attr('disabled', true);
        }
    });
});

$('#Can').click(function () {
    $('#myModal').css('display', 'none');
});

$('#Red').click(function () {
    $.ajax({
        url: "redbutton",
        method: 'POST',
        data: {
            name: $('select option:selected').text(),
            click: true
        },
        success: function (response) {
            if (typeof response.ticket === "undefined")
                location.reload()
            else
                $('#myModal').css('display', 'none');
                $('#ta').text(response.ticket);
                $('#tb').text(response.service);
                localStorage.setItem('ticket', response.ticket);
                localStorage.setItem('service', response.service);
                localStorage.setItem('hour', response.hour);
                localStorage.setItem('minute', response.minute);
                localStorage.setItem('second', response.second);
            }
    });
});

$('#Break').click(function () {
    $.ajax({
        url: "breakbutton",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            if (typeof response.ticket === "undefined")
                location.reload()
            else
                $('#ta').text(response.ticket);
                $('#tb').text(response.service);
                localStorage.setItem('ticket', response.ticket);
                localStorage.setItem('service', response.service);
                localStorage.setItem('hour', response.hour);
                localStorage.setItem('minute', response.minute);
                localStorage.setItem('second', response.second);
        }
    });
});

if (localStorage.getItem('ticket') === null) {
    localStorage.setItem('ticket', 'Текущий талон: ');
}

$('#Change').click(function () {
    $.ajax({
        url: "operatorbutton",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            localStorage.clear();
            window.location.href = "/service";
        }
    });
});

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


let id = setInterval(update, 500);
function update() {
    var date = new Date()
    var mint = 0
    var hort = 0
    if (localStorage.getItem('ticket') != null) $('#ta').text(localStorage.getItem('ticket'));
    if (localStorage.getItem('service') != null) $('#tb').text(localStorage.getItem('service'));
    if (localStorage.getItem('ticket_r') != null){
        $('#Delay').addClass('return');
        $('#Delay').attr("value", "Вернуть талон " + localStorage.getItem('ticket_r'));
        $('#Delay').removeAttr('disabled');
    }

    var seconds = date.getSeconds() - localStorage.getItem('second');
    if (seconds < 0) {
        seconds = 60 + seconds;
        mint = 1;
    }
    if (seconds < 10) seconds = '0' + seconds;
    if (isNaN(seconds)) {
        $('#time').css('visibility', 'hidden');
        $('#Replay, #Cancel, #Break, #Redirect').attr('disabled', true);
    }
    document.getElementById('sec').innerHTML = seconds;

    var minutes = date.getMinutes() - localStorage.getItem('minute') - mint;
    if (minutes < 0) {
        minutes = 60 + minutes;
        hort = 1;
    }
    if (minutes < 10) minutes = '0' + minutes;
    document.getElementById('min').innerHTML = minutes;

    var hours = date.getHours() - localStorage.getItem('hour') - hort;
    if (hours < 10) hours = '0' + hours;
    document.getElementById('hour').innerHTML = hours;

    if (hours === '00' && minutes === '00') {
        $('#time').css('visibility', 'visible');
        if (localStorage.getItem('ticket').search('Перерыв') !== -1) {
            $('#Replay, #Cancel, #Break, #Redirect, #Delay').attr('disabled', true);
        }
        else {
            $('#Replay, #Cancel, #Break, #Redirect, #Delay').removeAttr('disabled');
        }
    }

    if ($('#Delay').attr("value") == 'Отложить' && $('#ta').text() == 'Текущий талон: Нет талонов в очереди') {
        $('#Delay').attr('disabled', true);
    }

}