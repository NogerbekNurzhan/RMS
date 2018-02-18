$(function() {
    var tree = $('.data-tree').data('tree');
    var field = $('.data-tree').data('field');
    render_tree();

    function render_tree() {
        if(tree != undefined && field != undefined)
            $(".tree").replaceWith(make_ul(tree))
    }

    function make_ul(lst) {
        var html = $('<ul class="list-group w-100">');
        for(var name in lst)
            html.append(make_li(name, lst[name]))
        return html;
    }

    function make_li(name, elem) {
        var html = $('<li class="list-group-item w-100">');
        if (typeof(elem) == 'object') {
            html.append('<span class="btn btn-sm btn-primary w-100">'+ name + '</span>').append(make_ul(elem));
        }
        if (typeof(elem) != 'object'){
            html.append($('[name='+field+'][value='+elem+']').parent())
        }
        return html;
    }

    $("ul ul.list-group").hide();

    $("ul span").click(function() {
        $(this).next("ul").slideToggle();
    });
});