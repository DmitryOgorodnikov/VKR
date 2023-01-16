$(document).ready(function () {
    $.ajax({
        url: "statisticstableall",
        method: 'GET',
        data: {
            click: true
        },
        success: function (response) {
            var nt = []
            var ctx1 = document.getElementById('myChart1').getContext('2d');
            var myChart1 = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
                    datasets: [{
                        label: 'Число талонов',
                        data: response.nt,
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
                        text: 'Число талонов по месяцам',
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

            var ctx2 = document.getElementById('myChart2').getContext('2d');
            var myChart2 = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: response.services,
                    datasets: [{
                        label: 'Число обслуженных талонов',
                        data: response.stc,
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
                        text: 'Топ услуг',
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

            stat = response.stat
            for (var i = 0; i < stat.length; i++) {
                stat[i] = (stat[i] / 60).toFixed(2)
            }

            var ctx3 = document.getElementById('myChart3').getContext('2d');
            var myChart3 = new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: response.services,
                    datasets: [{
                        label: 'Среднее время обслуживания услуг',
                        data: response.stat,
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
                        text: 'Среднее время обслуживания по услугам (в минутах)',
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

