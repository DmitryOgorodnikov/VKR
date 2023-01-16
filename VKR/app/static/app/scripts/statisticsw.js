var myChart1;
var myChart2;

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

            $('.buttontable').prepend('<tr><td><button type="button" class="settings-btn" name="' + date_2.getFullYear() + ', ' + date_2.getMonth() + ', ' + date_2.getDate() +'">' + arr[0] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date_1.getFullYear() + ', ' + date_1.getMonth() + ', ' + date_1.getDate() + '">' + arr[1] + '</button></td>' +
                '<td><button type="button" class="settings-btn button-select" name="' + date.getFullYear() + ', ' + date.getMonth() + ', ' + date.getDate() + '" disabled>' + arr[2] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date1.getFullYear() + ', ' + date1.getMonth() + ', ' + date1.getDate() + '">' + arr[3] + '</button></td>' +
                '<td><button type="button" class="settings-btn" name="' + date2.getFullYear() + ', ' + date2.getMonth() + ', ' + date2.getDate() + '">' + arr[4] + '</button></td>' +
                '</tr>');

            var nw = [];
            var tc = [];
            var at = [];
            nw = response.nw;
            tc = response.tc;
            at = response.at;

            var ctx1 = document.getElementById('myChart1').getContext('2d');
            myChart1 = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: nw,
                    datasets: [{
                        label: 'Число талонов',
                        data: tc,
                        backgroundColor: [
                            'rgba(216, 27, 96, 0.6)',
                            'rgba(3, 169, 244, 0.6)',
                            'rgba(255, 152, 0, 0.6)',
                            'rgba(29, 233, 182, 0.6)',
                            'rgba(156, 39, 176, 0.6)',
                            'rgba(25, 75, 176, 0.6)',
                            'rgba(232, 67, 21, 0.6)',
                            'rgba(255, 221, 0, 0.6)',
                            'rgba(34, 255, 0, 0.6)',
                            'rgba(23, 1, 1, 0.6)',
                            'rgba(255, 140, 0, 0.6)',
                            'rgba(84, 110, 122, 0.6)'
                        ],
                        borderColor: [
                            'rgba(216, 27, 96, 1)',
                            'rgba(3, 169, 244, 1)',
                            'rgba(255, 152, 0, 1)',
                            'rgba(29, 233, 182, 1)',
                            'rgba(156, 39, 176, 1)',
                            'rgba(25, 75, 176, 1)',
                            'rgba(232, 67, 21, 1)',
                            'rgba(255, 221, 0, 1)',
                            'rgba(34, 255, 0, 1)',
                            'rgba(23, 1, 1, 1)',
                            'rgba(255, 140, 0, 1)',
                            'rgba(84, 110, 122, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Число талонов по окнам',
                        position: 'top',
                        fontSize: 16,
                        padding: 20
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                precision: 0,
                                min: 0
                            }
                        }]
                    }
                }
            });


            for (var i = 0; i < at.length; i++) {
                at[i] = (at[i] / 60).toFixed(1)
            }

            var ctx2 = document.getElementById('myChart2').getContext('2d');
            myChart2 = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: nw,
                    datasets: [{
                        label: 'Среднее время работы с талоном',
                        data: at,
                        backgroundColor: [
                            'rgba(216, 27, 96, 0.6)',
                            'rgba(3, 169, 244, 0.6)',
                            'rgba(255, 152, 0, 0.6)',
                            'rgba(29, 233, 182, 0.6)',
                            'rgba(156, 39, 176, 0.6)',
                            'rgba(25, 75, 176, 0.6)',
                            'rgba(232, 67, 21, 0.6)',
                            'rgba(255, 221, 0, 0.6)',
                            'rgba(34, 255, 0, 0.6)',
                            'rgba(23, 1, 1, 0.6)',
                            'rgba(255, 140, 0, 0.6)',
                            'rgba(84, 110, 122, 0.6)'
                        ],
                        borderColor: [
                            'rgba(216, 27, 96, 1)',
                            'rgba(3, 169, 244, 1)',
                            'rgba(255, 152, 0, 1)',
                            'rgba(29, 233, 182, 1)',
                            'rgba(156, 39, 176, 1)',
                            'rgba(25, 75, 176, 1)',
                            'rgba(232, 67, 21, 1)',
                            'rgba(255, 221, 0, 1)',
                            'rgba(34, 255, 0, 1)',
                            'rgba(23, 1, 1, 1)',
                            'rgba(255, 140, 0, 1)',
                            'rgba(84, 110, 122, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Среднее время работы с талоном (в минутах) по окнам',
                        position: 'top',
                        fontSize: 16,
                        padding: 20
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                min: 0
                            }
                        }]
                    }
                }
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


            var nw = [];
            var tc = [];
            var at = [];

            nw = response.nw;
            tc = response.tc;
            at = response.at;

            for (var i = 0; i < at.length; i++) {
                at[i] = (at[i] / 60).toFixed(2)
            }

            myChart1.data.labels = nw;
            myChart1.data.datasets[0].data = tc;
            myChart1.update();

            myChart2.data.labels = nw;
            myChart2.data.datasets[0].data = at;
            myChart2.update();
        }
    });
});

