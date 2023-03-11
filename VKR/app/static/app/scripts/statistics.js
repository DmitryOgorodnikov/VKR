$(document).ready(tickets);

function tickets() {
    $.ajax({
        url: "statisticstable",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            $('th').remove()
            $('tr').remove()
            var date = new Date()
            var date_1 = new Date()
            var date_2 = new Date()
            var date1 = new Date()
            var date2 = new Date()
            monthA = 'янв.,фев.,мар.,апр.,май.,июн.,июл.,авг.,сен.,окт.,ноя.,дек.'.split(',');
            weekA = 'вс,пн,вт,ср,чт,пт,сб,вс'.split(',');
            var dateOffset = (24 * 60 * 60 * 1000)

            date_1.setTime(date.getTime() - dateOffset);
            date_2.setTime(date_1.getTime() - dateOffset);
            date1.setTime(date.getTime() + dateOffset);
            date2.setTime(date1.getTime() + dateOffset);
            let arr = new Array();

            arr.push(weekA[date_2.getDay()] + ' - ' + date_2.getDate() + ' ' + monthA[date_2.getMonth()])
            arr.push(weekA[date_1.getDay()] + ' - ' + date_1.getDate() + ' ' + monthA[date_1.getMonth()])
            arr.push(weekA[date.getDay()] + ' - ' + date.getDate() + ' ' + monthA[date.getMonth()])
            arr.push(weekA[date1.getDay()] + ' - ' + date1.getDate() + ' ' + monthA[date1.getMonth()])
            arr.push(weekA[date2.getDay()] + ' - ' + date2.getDate() + ' ' + monthA[date2.getMonth()])
            if ($('.custom-checkbox').length === 0)
                $('.statistics-div-chld-two').prepend('<input id="auto" type="checkbox"><label class="custom-checkbox">Автоматически обновлять лог раз в 2 секунды</label>')
            $('.buttontable').prepend('<tr><td><button type="button" class="settings-btn" name="' + date_2.getFullYear() + ', ' + date_2.getMonth() + ', ' + date_2.getDate() + '">' + arr[0] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date_1.getFullYear() + ', ' + date_1.getMonth() + ', ' + date_1.getDate() + '">' + arr[1] + '</button></td>' +
                '<td><button type="button" class="settings-btn button-select" name="' + date.getFullYear() + ', ' + date.getMonth() + ', ' + date.getDate() + '" disabled>' + arr[2] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date1.getFullYear() + ', ' + date1.getMonth() + ', ' + date1.getDate() + '">' + arr[3] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date2.getFullYear() + ', ' + date2.getMonth() + ', ' + date2.getDate() + '">' + arr[4] + '</button></td>' +
                '</tr>');
            arr = response.listoftickets;
            $('.stattable').prepend('<th>Имя талона</th><th>Услуга</th><th>Статус</th><th>Время выдачи</th><th>Время вызова</th><th>Время закрытия</th><th>Окно</th><th>Оператор</th><th>Время пауз</th><th>Время обслуживания</th>');
            arr.forEach(function (item, i, arr) {
                var classname = ''
                if (item[10] > 600)
                    classname = 'red'
                else if (item[10] > 300)
                    classname = 'yellow'
                $('.stattable').prepend('<tr><td>' + item[0] + '</td>' +
                    '<td>' + item[1] + '</td>' +
                    '<td>' + item[2] + '</td>' +
                    '<td>' + item[3] + '</td>' +
                    '<td>' + item[4] + '</td>' +
                    '<td>' + item[5] + '</td>' +
                    '<td>' + item[6] + '</td>' +
                    '<td>' + item[7] + '</td>' +
                    '<td>' + item[8] + '</td>' +
                    '<td class="' + classname + '">' + item[9] + '</td>' +
                    '</tr>');
            });
        }
    });
}

$('table').on('click', '.settings-btn', function () {
    $.ajax({
        url: "statisticstable",
        method: 'GET',
        data: {
            date: this.name,
            click2: true
        },
        success: function (response) {
            var date = new Date(response.date)
            var date_1 = new Date()
            var date_2 = new Date()
            var date1 = new Date()
            var date2 = new Date()
            monthA = 'янв.,фев.,мар.,апр.,май.,июн.,июл.,авг.,сен.,окт.,ноя.,дек.'.split(',');
            weekA = 'вс,пн,вт,ср,чт,пт,сб,вс'.split(',');
            var dateOffset = (24 * 60 * 60 * 1000)

            date_1.setTime(date.getTime() - dateOffset);
            date_2.setTime(date_1.getTime() - dateOffset);
            date1.setTime(date.getTime() + dateOffset);
            date2.setTime(date1.getTime() + dateOffset);
            let arr = new Array();

            arr.push(weekA[date_2.getDay()] + ' - ' + date_2.getDate() + ' ' + monthA[date_2.getMonth()])
            arr.push(weekA[date_1.getDay()] + ' - ' + date_1.getDate() + ' ' + monthA[date_1.getMonth()])
            arr.push(weekA[date.getDay()] + ' - ' + date.getDate() + ' ' + monthA[date.getMonth()])
            arr.push(weekA[date1.getDay()] + ' - ' + date1.getDate() + ' ' + monthA[date1.getMonth()])
            arr.push(weekA[date2.getDay()] + ' - ' + date2.getDate() + ' ' + monthA[date2.getMonth()])

            $('th').remove()
            $('tr').remove()
            $('.buttontable').prepend('<tr><td><button type="button" class="settings-btn" name="' + date_2.getFullYear() + ', ' + date_2.getMonth() + ', ' + date_2.getDate() + '">' + arr[0] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date_1.getFullYear() + ', ' + date_1.getMonth() + ', ' + date_1.getDate() + '">' + arr[1] + '</button></td>' +
                '<td><button type="button" class="settings-btn button-select" name="' + date.getFullYear() + ', ' + date.getMonth() + ', ' + date.getDate() + '" disabled>' + arr[2] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date1.getFullYear() + ', ' + date1.getMonth() + ', ' + date1.getDate() + '">' + arr[3] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date2.getFullYear() + ', ' + date2.getMonth() + ', ' + date2.getDate() + '">' + arr[4] + '</button></td>' +
                '</tr>');
            arr = response.listoftickets;
            $('.stattable').prepend('<th>Имя талона</th><th>Услуга</th><th>Статус</th><th>Время выдачи</th><th>Время вызова</th><th>Время закрытия</th><th>Окно</th><th>Оператор</th><th>Время пауз</th><th>Время обслуживания</th>');
            arr.forEach(function (item, i, arr) {
                var classname = ''
                if (item[10] > 600)
                    classname = 'red'
                else if (item[10] > 300)
                    classname = 'yellow'
                $('.stattable').prepend('<tr><td>' + item[0] + '</td>' +
                    '<td>' + item[1] + '</td>' +
                    '<td>' + item[2] + '</td>' +
                    '<td>' + item[3] + '</td>' +
                    '<td>' + item[4] + '</td>' +
                    '<td>' + item[5] + '</td>' +
                    '<td>' + item[6] + '</td>' +
                    '<td>' + item[7] + '</td>' +
                    '<td>' + item[8] + '</td>' +
                    '<td class="' + classname + '">' + item[9] + '</td>' +
                    '</tr > ');
            });
        }
    });
});

document.getElementById("sheetjsexport").addEventListener('click', function () {
    var wb = XLSX.utils.book_new();
    var Heading = [
        ['Имя талона', 'Услуга', 'Статус', 'Время выдачи', 'Время закрытия', 'Время вызова', 'Окно', 'Оператор', 'Время пауз', 'Время обслуживания']
    ];
    var ws = XLSX.utils.aoa_to_sheet(Heading);
    XLSX.utils.sheet_add_dom(ws, document.getElementById("TableToExport"), { origin: "A2" })
    XLSX.utils.book_append_sheet(wb, ws, "Лист 1");
    var name1 = $('a.btn-def')[0].textContent
    name1 = name1.trim()
    var name2 = $('td button:disabled')[0].textContent
    XLSX.writeFile(wb, name1 + " - " + name2 + "xlsx");
});

let interval;

document.addEventListener('change', function () {
    var chk = event.target;
    if (chk.id === 'auto' && chk.type === 'checkbox' && chk.checked === true) {
        interval = setInterval(tickets, 2000);
    }
    else
        clearInterval(interval);
});