$(document).ready(function () {
    $.ajax({
        url: "statisticstablew",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
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

            $('.buttontable').prepend('<tr><td><button type="button" class="settings-btn" name="' + date_2.getFullYear() + ', ' + date_2.getMonth() + ', ' + date_2.getDate() + '">' + arr[0] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date_1.getFullYear() + ', ' + date_1.getMonth() + ', ' + date_1.getDate() + '">' + arr[1] + '</button></td>' +
                '<td><button type="button" class="settings-btn button-select" name="' + date.getFullYear() + ', ' + date.getMonth() + ', ' + date.getDate() + '" disabled>' + arr[2] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date1.getFullYear() + ', ' + date1.getMonth() + ', ' + date1.getDate() + '">' + arr[3] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date2.getFullYear() + ', ' + date2.getMonth() + ', ' + date2.getDate() + '">' + arr[4] + '</button></td>' +
                '</tr>');
            arr = response.listoflogwindows;
            $('.stattable').prepend('<th>Окно</th><th>Оператор</th><th>Время входа</th><th>Время выхода</th><th>Время работы</th><th>Время пауз</th><th>Число талонов</th><th>Среднее время обслуживания</th>');
            arr.forEach(function (item, i, arr) {
                var classname = ''
                if (item[8] > 600)
                    classname = 'red'
                else if (item[8] > 300)
                    classname = 'yellow'
                $('.stattable').prepend('<tr><td>' + item[0] + '</td>' +
                    '<td>' + item[1] + '</td>' +
                    '<td>' + item[2] + '</td>' +
                    '<td>' + item[3] + '</td>' +
                    '<td>' + item[4] + '</td>' +
                    '<td>' + item[5] + '</td>' +
                    '<td>' + item[6] + '</td>' +
                    '<td class="' + classname +'">' + item[7] + '</td>' +
                    '</tr>');
            });
        }
    });
});

$('table').on('click', '.settings-btn', function () {
    $.ajax({
        url: "statisticstablew",
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
            arr = response.listoflogwindows;
            $('.stattable').prepend('<th>Окно</th><th>Оператор</th><th>Время входа</th><th>Время выхода</th><th>Время работы</th><th>Время пауз</th><th>Число талонов</th><th>Среднее время обслуживания</th>');
            arr.forEach(function (item, i, arr) {
                var classname = ''
                if (item[8] > 600)
                    classname = 'red'
                else if (item[8] > 300)
                    classname = 'yellow'
                $('.stattable').prepend('<tr><td>' + item[0] + '</td>' +
                    '<td>' + item[1] + '</td>' +
                    '<td>' + item[2] + '</td>' +
                    '<td>' + item[3] + '</td>' +
                    '<td>' + item[4] + '</td>' +
                    '<td>' + item[5] + '</td>' +
                    '<td>' + item[6] + '</td>' +
                    '<td class="' + classname +'">' + item[7] + '</td>' +
                    '</tr>');
            });
        }
    });
});

