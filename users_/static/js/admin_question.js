function CreateNewAnswer() {
    $.ajax({
        type: "POST",
        url: "ajax_new_answer",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            new_answer: $('textarea[name=new_answer]')[0].value,
            correct: $('input[name=correct]')[0].checked
        }),
        success: function (json) {
            if (json.success) {
                var textarea = $('textarea[name=new_answer]')[0].value;
                $('tr.add_new_button').show();
                $('tr.add_new').hide();
                var tr = document.createElement("tr");
                tr.innerHTML = '<td class="title">' +
                                   '<a class="title" id="' +
                                        json.new_answer_id + '">' + textarea +
                                   '</a>' +
                                 '</td>' +
                                 '<td class="correct">' +
                                   json.correct +
                                 '</td>' +
                                 '<td class="edit">' +
                                   '<a class="edit">edit</a>' +
                                 '</td>' +
                                 '<td class="delete">' +
                                   '<a class="delete">delete</a>' +
                                 '</td>';
                $('table tbody tr.add_new').before(tr);
                $('textarea[name=new_answer]')[0].value = "";
                $('p#None').hide();
            }
            $('output').html(json.message);
            $('output').show();
            $('output').fadeOut(5000);
        }
    });
}

function DeleteAnswer(e) {
    $.ajax({
        type: "POST",
        url: "ajax_delete_answer",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            delete_answer: e.target.parentElement.parentElement.
                             firstElementChild.firstElementChild.id
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
        DeleteAnswer(e);
    });
    $('button#add_new')[0].onclick = function () {
        $('tr.add_new').show();
        $('tr.add_new_button').hide();
    };
    $('button#cancel')[0].onclick = function () {
        $('textarea')[0].value = "";
        $('tr.add_new_button').show();
        $('tr.add_new').hide();
    };
});