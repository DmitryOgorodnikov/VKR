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
                var keys = Object.keys(item);
                if (keys.length == 1) {
                    if (item[keys[0]] == true)
                        ch = 'checked';
                    else {
                        ch = '';
                    }
                    $('table').prepend('<tr>' +
                        '<td class="table1wc"><input type="checkbox" ' + ch + ' id="check" name="' + keys[0] + '">' + '</td>' +
                        '<td class="table1w" name="' + keys[0] + '">' + keys[0] + '</td>' +
                        '</tr> ');
                }
                else {
                    var keys2 = Object.keys(item[keys[0]]);
                    for (let i = 0; i < keys2.length; i++) {
                        if (item[keys[0]][keys2[i]] == true)
                            ch = 'checked';
                        else
                            ch = '';
                        $('table').prepend('<tr class="table1wcd">' +
                            '<td class= "table1wc"><input type = "checkbox" ' + ch + ' id = "check" name = "' + keys2[i] + '">' + '</td >' +
                            '<td class="table1w" name="' + keys2[i] + '">' + keys2[i] + '</td>' +
                            '</tr > ');
                    }
                    if (item[keys[1]] == true)
                        ch = 'checked';
                    else {
                        ch = '';
                    }
                    $('table').prepend('<tr>'+
                        '<td class="table1wc"><input type="checkbox" ' + ch + ' id="check" name="' + keys[1] + '">' + '</td>' +
                        '<td class="table1w" name="' + keys[1] + '">' + keys[1] + '</td>' +
                        '</tr> ');
                }
            });
        }
    });
});

$('.tablediv-input').click(function () {
    var result = $('input', 'td');
    var listofcheck = []
    for (var i = 0; i < result.length; i++) {
        let check = { [result[i].name]: result[i].checked};
        listofcheck.push(check);
    };
    $.ajax({
        url: "wchange",
        method: 'POST',
        data: {
            listofcheck: JSON.stringify(listofcheck),
            click2: true
        },
        success: function (response) {
            window.location.href = "../ops"
        }
    });
});