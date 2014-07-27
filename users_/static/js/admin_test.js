function CreateNewQuestion() {
    $.ajax({
        type: "POST",
        url: "ajax_new_question",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            new_question: $('textarea[name=new_question]')[0].value
        }),
        success: function (json) {
            if (json.success) {
                var textarea = $('textarea[name=new_question]')[0].value;
                $('tr.add_new_button').show();
                $('tr.add_new').hide();
                var tr = document.createElement("tr");
                tr.innerHTML = '<td class="title">' +
                                   '<a class="title" href="' +
                                     json.new_question_id + '" id="' +
                                     json.new_question_id + '">' + textarea +
                                   '</a>' +
                                 '</td>' +
                                 '<td class="edit">' +
                                   '<a class="edit">edit</a>' +
                                 '</td>' +
                                 '<td class="delete">' +
                                   '<a class="delete">delete</a>' +
                                 '</td>';
                $('table tbody tr.add_new').before(tr);
                $('textarea[name=new_question]')[0].value = "";
                $('p#None').hide();
            }
            $('output').html(json.message);
            $('output').show();
            $('output').fadeOut(5000);
        }
    });
}
var c;
function DeleteQuestion(e) {
    c = e;
    $.ajax({
        type: "POST",
        url: "ajax_delete_question",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            delete_question: e.target.parentElement.parentElement.
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
        DeleteQuestion(e);
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