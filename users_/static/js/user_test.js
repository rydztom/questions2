function SendResult () {
    var collected_answers = collect_answers();
    var answers = collected_answers[0];
    var all_marked = collected_answers[1];
    if (!all_marked) {
        $('output').html("U have to answer for all questions!");
        $('output').show();
        $('output').fadeOut(5000);
        return false
    };
    var send_mail = $('input[name=send_mail]')[0].checked;
    $.ajax({
        type: "POST",
        url: "ajax_send_result",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]')[0].value,
            result: answers,
            send_mail: send_mail
        }),
        success: function (json) {
            $('output').html("U scored "+json.score+" points");
            $('output').show();
        }
    });
}

function collect_answers () {
    var all_marked = true;
    var result = {};
    $('div.question').each( function (k,v) {
        var answers = [];
        $('input:checked', v).each( function (key,value) {
            answers.push(value.value);
        });
        if (answers.length === 0) {
            all_marked = false;
        }
        result[v.id] = answers;
    });
    return [result, all_marked];
}