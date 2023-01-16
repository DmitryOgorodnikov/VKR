$(document).ready(function () {
    $.ajax({
        url: "kioskbtn",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            arr = response.serviceslist;
            arr.reverse();
            arr.forEach(function (item, i, arr) {
                if (item['status'] != true)
                    delete arr[i]
                else
                    $('.kiosk-div').prepend('<div class="kiosk-div-button settings-btn" id="buttonticket" name="' + item['rusname'] + '"><p>' + item['rusname'] + '</p></div>');
            });
                $('#print-text').html(response.ticketname)

                var date = new Date()

                var hours = date.getHours()
                if (hours < 10) hours = '0' + hours
                document.getElementById('hour').innerHTML = hours

                var minutes = date.getMinutes()
                if (minutes < 10) minutes = '0' + minutes
                document.getElementById('min').innerHTML = minutes

                var days = date.getDate()
                if (days < 10) days = '0' + days
                document.getElementById('day').innerHTML = days

                var months = date.getMonth() + 1
                if (months < 10) months = '0' + months
                document.getElementById('month').innerHTML = months

                var years = date.getFullYear()
                document.getElementById('year').innerHTML = years
        }
    });
});

$('.kiosk-div').on('click', '#buttonticket', function () {
    $.ajax({
        url: "kbutton",
        method: 'POST',
        data: {
            name: $(this).attr("name"),
            click: true
        },
        success: function (response) {
            var modal = $modal({
                title: 'Номер вашего талона',
                content: '<p>' + response.ticketname + '</p>',
            });
            modal.show();
            $('#print-text').html(response.ticketname)
            callPrint();
            setTimeout(() => { location.reload();  }, 5000);

        }
    });
});

function callPrint() {
    var printTitle = document.getElementById('print-title').innerHTML;
    var printText = document.getElementById('print-text').innerHTML;
    var windowPrint = window.open('', '', 'left=50,top=50,width=800,height=640,toolbar=0,scrollbars=1,status=0');
    windowPrint.document.write('<p><center style="font-size: 250px;">' + printTitle + '</center></p>');
    windowPrint.document.write('<p><center style="font-size: 250px;">' + printText + '</center></p>');

    var date = new Date()

    var hours = date.getHours()
    if (hours < 10) hours = '0' + hours

    var minutes = date.getMinutes()
    if (minutes < 10) minutes = '0' + minutes

    var seconds = date.getSeconds()
    if (seconds < 10) seconds = '0' + seconds

    var days = date.getDate()
    if (days < 10) days = '0' + days

    var months = date.getMonth() + 1
    if (months < 10) months = '0' + months

    var years = date.getFullYear()

    document.getElementById('year').innerHTML = years
    windowPrint.document.write('<p><center style="font-size: 100px;">' + hours + ':' + minutes + ':' + seconds + ' ' + days + '.' + months + '.' + years + '</center></p>');
    windowPrint.document.close();
    windowPrint.focus();
    windowPrint.print();
    windowPrint.close();
}

let id = setInterval(update, 60000);
function update() {
    var date = new Date()

    var hours = date.getHours()
    if (hours < 10) hours = '0' + hours
    document.getElementById('hour').innerHTML = hours

    var minutes = date.getMinutes()
    if (minutes < 10) minutes = '0' + minutes
    document.getElementById('min').innerHTML = minutes

    var days = date.getDate()
    if (days < 10) days = '0' + days
    document.getElementById('day').innerHTML = days

    var months = date.getMonth() + 1
    if (months < 10) months = '0' + months
    document.getElementById('month').innerHTML = months

    var years = date.getFullYear()
    document.getElementById('year').innerHTML = years
}