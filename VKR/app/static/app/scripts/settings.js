var modal;
var name;
del_finction = null;

$(document).ready(function () {
    var elemTarget;
    modal = $modal({
        title: '<h2>Вы уверены?</h2>',
        content: '<h3>Пользователь будет удален окончательно, но он не исчезнет из описания талонов, закрытых им.</h3>',
        footerButtons: [
            { class: 'btn btn-2', text: 'Да', handler: 'Ok' },
            { class: 'btn btn-1', text: 'Отмена', handler: 'Cancel' }
        ]
    });
    $.ajax({
        url: "settingstable",
        method: 'POST',
        data: {
            click: true
        },
        success: function (response) {
            for (i = 0; i < response.user.length; i++) {
                $('table').prepend('<tr><td class="table1">Логин: ' + response.user[i][1] + '</td>' + '<td class="table2">ФИО: ' + response.user[i][2] +
                    '</td><td class="table3"></td> <td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' +
                    response.user[i][0] + '" value="Настроить" id="Edit"> </td> <td class="table4"> <input type="button" class="btn btn-default btn-index" name= "' +
                    response.user[i][0] + '" value="Удалить" id="Del"></td> </tr>');
            }
        }
    });
});

$('table').on('click', '#Del', function () {
    name = this.name;
    modal.show();
});

$('body').on('click', "[data-handler='Ok']", function () {
    $.ajax({
        url: "delbutton",
        method: 'POST',
        data: {
            idbutton: name,
            click: true
        },
        success: function (response) {
            location.reload();
        }
    });
    modal.hide();
});

$('body').on('click', "[data-handler='Cancel']", function () {
    modal.hide();
});


$('table').on('click', '#Edit', function () {
    $.ajax({
        url: "edituser",
        method: 'POST',
        data: {
            idbutton: this.name,
            click: true
        },
        success: function (response) {
            window.location.href = "../editer"
        }
    });
});