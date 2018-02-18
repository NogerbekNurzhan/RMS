$(document).ready(function () {
    $('.collapse')
        .on('shown.bs.collapse', function(event) {
            event.stopPropagation();
            $(this)
                .parent().parent()
                .find(".fa-eye")
                .removeClass("fa-eye")
                .addClass("fa-eye-slash");
        }).on('hidden.bs.collapse', function(event) {
            event.stopPropagation();
            $(this)
                .parent().parent()
                .find(".fa-eye-slash")
                .removeClass("fa-eye-slash")
                .addClass("fa-eye");
        });
});