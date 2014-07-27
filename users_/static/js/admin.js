function CreateNewTest() {
    $.ajax({
        type: "POST",
        url: "ajax_new_test",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            new_test: $('input[name=new_test]')[0].value
        }),
        success: function (json) {
            if (json.success) {
                var input = $('input[name=new_test]')[0].value;
                $('tr.add_new_button').show();
                $('tr.add_new').hide();
                var tr = document.createElement("tr");
                tr.innerHTML = '<td class="title">' +
                                   '<a class="title" href="admin/' +
                                     json.test_id + '">' + input +
                                   '</a>' +
                                 '</td>' +
                                 '<td class="edit">' +
                                   '<a class="edit">edit</a>' +
                                 '</td>' +
                                 '<td class="delete">' +
                                   '<a class="delete">delete</a>' +
                                 '</td>';
                $('table tbody tr.add_new').before(tr);
                $('input[name=new_test]')[0].value = "";
                $('p#None').hide();
            }
            $('output').html(json.message);
            $('output').show();
            $('output').fadeOut(5000);
        }
    });
}

function DeleteTest(e) {
    $.ajax({
        type: "POST",
        url: "ajax_delete_test",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            delete_test: e.target.parentElement.parentElement.
                           firstElementChild.firstElementChild.innerText
        }),
        success: function (json) {
            e.target.parentElement.parentElement.remove();
            $('output').html(json.message);
            $('output').show();
            $('output').fadeOut(5000);
            if ($('table tr').size() < 4) {
                $('p#None').show();
            }
        }
    });
}

$(function () {
    $('table').delegate('a.delete', 'click', function (e) {
        DeleteTest(e);
    });
    $('button#add_new')[0].onclick = function () {
        $('tr.add_new').show();
        $('tr.add_new_button').hide();
    };
    $('button#cancel')[0].onclick = function () {
        $('input[name=new]')[0].value = "";
        $('tr.add_new_button').show();
        $('tr.add_new').hide();
    };
});