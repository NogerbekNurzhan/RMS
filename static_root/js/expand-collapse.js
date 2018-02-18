$(function () {
    $('#expand-collapse').on('click',function(){
        var allCollapsed = true;
        $('.expand-collapse-block .collapse').each(function(i, block){
            if($(block).hasClass('show')) {
                allCollapsed = false;
            }
        });
        $('.expand-collapse-block .collapse').each(function(i, block){
            if (allCollapsed) {
                $(block).collapse('show');
            } else {
                $(block).collapse('hide');
            }
        });
    });
});

$(function () {
    $('#expand-collapse-group-task').on('click',function(){
        var allCollapsed = true;
        $('.group-task-block .collapse').each(function(i, block){
            if($(block).hasClass('show')) {
                allCollapsed = false;
            }
        });

        $('.group-task-block .collapse').each(function(i, block){
            if (allCollapsed) {
                $(block).collapse('show');
            } else {
                $(block).collapse('hide');
            }
        });
    });
});

$(function () {
    $('#expand-collapse-user-characteristic').on('click',function(){
        var allCollapsed = true;
        $('.user-characteristic-block .collapse').each(function(i, block){
            if($(block).hasClass('show')) {
                allCollapsed = false;
            }
        });
        $('.user-characteristic-block .collapse').each(function(i, block){
            if (allCollapsed) {
                $(block).collapse('show');
            } else {
                $(block).collapse('hide');
            }
        });
    });
});