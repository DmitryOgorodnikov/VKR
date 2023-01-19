$(document).ready(function () {
    $.ajax({
        url: "settingsm",
        method: 'GET',
        data: {
            click1: true
        },
        success: function (response) {
            opsname = response.opsname;
            printcheck = response.printcheck;
            $('table').prepend('<tr><td class="table1w" name="opsname"> Номер ОПС: </td>' +
                '<td class="table1w" name="opsname">' + '<input type="text" id="opsname" class="form-control" value="' + opsname +'" ></td>' +
                '</tr > ');
            if (printcheck == true)
                ch = 'checked'
            else
                ch = ''
            $('table').append('<tr><td class="table1w" name="printcheck"> Печать талонов: </td>' +
                '<td class="table1w" name="printcheck">' + '<input type="checkbox" ' + ch + ' id="printcheck">' + '</td>' +
                '</tr > ');
        }
    });
});

$('.tablediv-input').click(function () {
    var result = $('input', 'td');
    var listofsettings = []
    listofsettings.push(result[0].value)
    listofsettings.push(result[1].checked)
    JSON.stringify(listofsettings);
    $.ajax({
        url: "settingsm",
        method: 'POST',
        data: {
            listofsettings: listofsettings.join(' '),
            click2: true
        },
        success: function (response) {
            window.location.href = "./settingsm"
        }
    });
});