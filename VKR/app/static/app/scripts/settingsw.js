$(document).ready(function () {
    $.ajax({
        url: "settingswtable",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            for (i = response.window.length - 1; i >= 0; i--) {
                if (response.window[i][1] == true)
                    $('table').prepend('<tr><td class="table1 table5">Окно: ' + response.window[i][0] + '</td>' +
                        '<td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' + response.window[i][0] + '" value="Настроить" id="windowchange"></td>' +
                        '<td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' + response.window[i][0] + '" value="Отключить" id="windowstatus"></td>' +
                        '</tr > ');
                else
                    $('table').prepend('<tr><td class="table1 table5">Окно: ' + response.window[i][0] + '</td>' +
                        '<td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' + response.window[i][0] + '" value="Настроить" id="windowchange"></td>' +
                        '<td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' + response.window[i][0] + '" value="Включить" id="windowstatus"></td>' +
                        '</tr > ');
            }
        }
    });
});

$('#Add').click(function () {
    $.ajax({
        url: "addwindow",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            location.reload();
        }
    });
});

$('table').on('click', '#windowstatus', function () {
    $.ajax({
        url: "changestatusw",
        method: 'POST',
        data: {
            idwindow: this.name,
            action: this.value,
            click: true
        },
        success: function (response) {
            location.reload();
        }
    });
});

$('table').on('click', '#windowchange', function () {
    $.ajax({
        url: "changeservicew",
        method: 'POST',
        data: {
            idwindow: this.name,
            click: true
        },
        success: function (response) {
            window.location.href = "settingswchange"
        }
    });
});
