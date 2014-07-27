var li;
function CreateNewTest() {
    $.ajax({
        type: "POST",
        url: "ajax_new_test",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            new_test: $('input[name=new_test]')[0].value,
        }),
        success: function (json) {
            if(json.success) {
                var input = $('input[name=new_test]')[0].value;
                $('p#add_new').show();
                $('div.add_new').hide();
                li = document.createElement("li");
                li.innerHTML = '<a class="test">'+input+
                    '</a> <a class="delete">delete</a>';
                $('ul#tests_list')[0].appendChild(li);
                input = "";
            }
            $('output').html(json.message);
        }
        
    });
};
function DeleteTest(e) {
    $.ajax({
        type: "POST",
        url: "ajax_delete_test",
        dataType: "json",
        async: true,
        data: JSON.stringify({
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]')[0].value,
            delete_test: e.target.parentElement.firstChild.innerText
        }),
        success: function (json) {
            e.target.parentElement.remove();
            $('output').html(json.message);
        }
        
    });
};

$(function() {
$('ul#tests_list').delegate('a.delete', 'click', function(e) {
    DeleteTest(e);
    console.log($(this));
    console.log(e);
    console.log(e.target);
    console.log(e.target.parentElement);
});
$('li a.delete').onclick = function(e) {
};
$('p#add_new')[0].onclick = function() {
    $('div.add_new').show();
    $('p#add_new').hide();
};
$('button#cancel')[0].onclick = function() {
    $('input[name=new_test]')[0].value = "";
    $('p#add_new').show();
    $('div.add_new').hide();
};
});