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
                    $('table').prepend('<tr id="' + keys[0] +'">' +
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
                        $('table').prepend('<tr class="table1wcd" id="' + keys[1] +'">' +
                            '<td class= "table1wc"><input type = "checkbox" ' + ch + ' id = "check" name = "' + keys2[i] + '">' + '</td >' +
                            '<td class="table1w" name="' + keys2[i] + '">' + keys2[i] + '</td>' +
                            '</tr > ');
                    }
                    if (item[keys[1]] == true)
                        ch = 'checked';
                    else {
                        ch = '';
                    }
                    $('table').prepend('<tr id="' + keys[1] +'">'+
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


document.addEventListener('change', function () {
    var chk = event.target;
    var chkpar = chk.parentNode.parentNode;
    var chkapsd;
    var cheks;
    var cheksup;
    var cheksdown;
    var count = 0;

    if (chk.tagName === 'INPUT' && chk.type === 'checkbox') {
        if (chkpar.className === 'table1wcd' && chk.checked === false) {
            chkapsd = $(chkpar).prevAll().not('.table1wcd')[0];
            cheksup = $(chkpar).prevUntil('tr:not(.table1wcd)');
            cheksdown = $(chkpar).nextUntil('tr:not(.table1wcd)');

            for (var i = 0; i < cheksup.length; i++) {
                if (cheksup[i].children[0].children[0].checked === true) {
                    count += 1;
                }
            }
            for (var i = 0; i < cheksdown.length; i++) {
                if (cheksdown[i].children[0].children[0].checked === true) {
                    count += 1;
                }
            }
            if (count === 0) {
                chkapsd.children[0].children[0].checked = false;
            }
        }
        else if (chkpar.className === 'table1wcd' && chk.checked === true) {
            chkapsd = $(chkpar).prevAll().not('.table1wcd')[0];
            chkapsd.children[0].children[0].checked = true;
        }
        if (chkpar.className === '') {
            cheks = chkpar.children[0].children[0].checked
            chkapsd = $(chkpar).nextUntil('tr:not(.table1wcd)');
            for (var i = 0; i < chkapsd.length; i++) {
                chkapsd[i].children[0].children[0].checked = cheks;
            }
        }
    }
});