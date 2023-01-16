$(document).ready(function () {
    $.ajax({
        url: "servicestable",
        method: 'GET',
        data: {
            click2: true
        },
        success: function (response) {
            arr = response.serviceslist;
            arr.reverse();
            arr.forEach(function (item, i, arr) {
                if (item['status'] == true)
                    ch = 'checked'
                else
                    ch = ''
                $('table').prepend('<tr><td class="table1w" name="' + item['name'] + '">' + item['rusname'] + '</td>' +
                    '<td class="table1w" name="' + item['name'] + '">' + '<input type="checkbox" ' + ch +  ' id="check">'  + '</td>' +
                    '</tr > ');
            });
        }
    });
});

$('.tablediv-input').click(function () {
    var result = $('input', 'td');
    var listofcheck = []
    for (var i = 0; i < result.length; i++) {
        listofcheck.push(result[i].checked)
    }
    JSON.stringify(listofcheck);
    $.ajax({
        url: "wchange",
        method: 'POST',
        data: {
            listofcheck: listofcheck.join(' '),
            click2: true
        },
        success: function (response) {
            window.location.href = "../ops"
        }
    });
});