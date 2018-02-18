function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// GROUP TASK
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_group_task_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#group-task-list").html(data.html_group_task);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_group_task_form);
                }
            }
        });
        return false;
    };
    // Create group task
    $("#group-task-add-button").click(loadForm);
    $("#modal").on("submit", ".js-group-task-add-form", saveForm);
    // Update group task
    $("#group-task-list").on("click", "#js-edit-group-task-button", loadForm);
    $("#modal").on("submit", ".js-group-task-edit-form", saveForm);
});

// GROUP TASK COMMENT
$('.group-task-block').on('submit', '.group-task-comment-form', function(event) {
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".group-task-comments").html(data.html_group_task_comment);
                comment.find(".group-task-comment-number").html(data.html_group_task_comment_number);
            }
            else {
                current_group.find(".group-task-comment-form").html(data.html_group_task_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// TASK
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_task_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#task-list").html(data.html_task);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_task_form);
                }
            }
        });
        return false;
    };
    // Create Task
    $("#task-add-button").click(loadForm);
    $("#modal").on("submit", ".js-task-add-form", saveForm);
    // Update Task
    $("#task-list").on("click", "#js-edit-task-button", loadForm);
    $("#modal").on("submit", ".js-task-edit-form", saveForm);
});

// TASK COMMENT
$('.task-block').on('submit', '.task-comment-form', function(event){
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".task-comments").html(data.html_task_comment);
                comment.find(".task-comment-number").html(data.html_task_comment_number);
            }
            else {
                current_group.find(".task-comment-form").html(data.html_task_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// FUNCTION
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_function_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#function-list").html(data.html_function);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_function_form);
                }
            }
        });
        return false;
    };
    // Create FUNCTION
    $("#function-add-button").click(loadForm);
    $("#modal").on("submit", ".js-function-add-form", saveForm);
    // Update FUNCTION
    $("#function-list").on("click", "#js-edit-function-button", loadForm);
    $("#modal").on("submit", ".js-function-edit-form", saveForm);
});

// FUNCTION COMMENT
$('.function-block').on('submit', '.function-comment-form', function(event){
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".function-comments").html(data.html_function_comment);
                comment.find(".function-comment-number").html(data.html_function_comment_number);
            }
            else {
                current_group.find(".function-comment-form").html(data.html_function_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// USER CHARACTERISTIC
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_user_characteristic_form);
                $("#user-class").autocomplete({
                    source: "/account/dashboard/projects/user_characteristic_autocomplete/",
                    minLength: 1,
                    select: function( event, ui ){
                        $("#user-class").val(ui.item.value);
                        $("#user-symbol").val(ui.item.user_symbol);
                        $("#user-description").val(ui.item.user_description);
                        return false;
                    }
                });
            }
        });
    };
    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#user-characteristic-list").html(data.html_user_characteristic);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_user_characteristic_form);
                    $("#user-class").autocomplete({
                        source: "/account/dashboard/projects/user_characteristic_autocomplete/",
                        minLength: 1,
                        select: function( event, ui ){
                            $("#user-class").val(ui.item.value);
                            $("#user-symbol").val(ui.item.user_symbol);
                            $("#user-description").val(ui.item.user_description);
                            return false;
                        }
                    });
                }
            }
        });
        return false;
    };
    // Create User Characteristic
    $("#user-characteristic-add-button").click(loadForm);
    $("#modal").on("submit", ".js-user-characteristic-add-form", saveForm);
    // Update User Characteristic
    $("#user-characteristic-list").on("click", "#js-edit-user-characteristic-button", loadForm);
    $("#modal").on("submit", ".js-user-characteristic-edit-form", saveForm);
});

// USER CHARACTERISTIC COMMENT
$('.user-characteristic-block').on('submit', '.user-characteristic-comment-form', function(event) {
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".user-characteristic-comments").html(data.html_user_characteristic_comment);
                comment.find(".user-characteristic-comment-number").html(data.html_user_characteristic_comment_number);
            }
            else {
                current_group.find(".user-characteristic-comment-form").html(data.html_user_characteristic_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// PROJECT MEMBER
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_project_member_form);
                $('#id_user').djangoSelect2();
                $('#id_role').djangoSelect2();
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#project-member-table tbody").html(data.html_project_member);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_project_member_form);
                    $('#id_user').djangoSelect2();
                    $('#id_role').djangoSelect2();
                }
            }
        });
        return false;
    };
    // Add project member
    $("#project-member-add-button").click(loadForm);
    $("#modal").on("submit", ".js-project-member-add-form", saveForm);
});

// GROUP REQUIREMENT TYPE
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-lg").modal("show");
            },
            success: function (data) {
                $("#modal-lg .modal-content").html(data.html_group_requirement_type_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#group-requirement-type-list").html(data.html_group_requirement_type);
                    $("#modal-lg").modal("hide");
                }
                else {
                    $("#modal-lg .modal-content").html(data.html_group_requirement_type_form);
                }
            }
        });
        return false;
    };

    // Create Group Requirement Type
    $("#group-requirement-type-add-button").click(loadForm);
    $("#modal-lg").on("submit", ".js-group-requirement-type-add-form", saveForm);
});

// PURPOSE
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_purpose_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#purpose-list").html(data.html_purpose);
                    $("#purpose-top").html(data.html_purpose_top);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_purpose_form);
                }
            }
        });
        return false;
    };
    // Create Purpose
    $("#purpose-add-button").click(loadForm);
    $("#modal").on("submit", ".js-purpose-add-form", saveForm);
    // Update Purpose
    $("#purpose-list").on("click", "#js-edit-purpose-button", loadForm);
    $("#modal").on("submit", ".js-purpose-edit-form", saveForm);
});

// PURPOSE COMMENT
$('.purpose-block').on('submit', '.purpose-comment-form', function(event){
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".purpose-comments").html(data.html_purpose_comment);
                comment.find(".purpose-comment-number").html(data.html_purpose_comment_number);
            }
            else {
                current_group.find(".purpose-comment-form").html(data.html_purpose_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// CREATION GOAL
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_creation_goal_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#creation-goal-list").html(data.html_creation_goal);
                    $("#creation-goal-top").html(data.html_creation_goal_top);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_creation_goal_form);
                }
            }
        });
        return false;
    };
    // Create Creation Goal
    $("#creation-goal-add-button").click(loadForm);
    $("#modal").on("submit", ".js-creation-goal-add-form", saveForm);
    // Update Creation Goal
    $("#creation-goal-list").on("click", "#js-edit-creation-goal-button", loadForm);
    $("#modal").on("submit", ".js-creation-goal-edit-form", saveForm);
});

// CREATION GOAL COMMENT
$('.creation-goal-block').on('submit', '.creation-goal-comment-form', function(event){
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".creation-goal-comments").html(data.html_creation_goal_comment);
                comment.find(".creation-goal-comment-number").html(data.html_creation_goal_comment_number);
            }
            else {
                current_group.find(".creation-goal-comment-form").html(data.html_creation_goal_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// OBJECT INFORMATION
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_object_information_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#object-information-list").html(data.html_object_information);
                    $("#object-information-top").html(data.html_object_information_top);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_object_information_form);
                }
            }
        });
        return false;
    };
    // Create Object Information
    $("#object-information-add-button").click(loadForm);
    $("#modal").on("submit", ".js-object-information-add-form", saveForm);
    // Update Object Information
    $("#object-information-list").on("click", "#js-edit-object-information-button", loadForm);
    $("#modal").on("submit", ".js-object-information-edit-form", saveForm);
});

// OBJECT INFORMATION COMMENT
$('.object-information-block').on('submit', '.object-information-comment-form', function(event){
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".object-information-comments").html(data.html_object_information_comment);
                comment.find(".object-information-comment-number").html(data.html_object_information_comment_number);
            }
            else {
                current_group.find(".object-information-comment-form").html(data.html_object_information_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// GROUP REQUIREMENT (GENERAL)
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_group_requirement_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#group-requirement-list").html(data.html_group_requirement);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_group_requirement_form);
                }
            }
        });
        return false;
    };
    // Create Group Requirement
    $("#group-requirement-add-button").click(loadForm);
    $("#modal").on("submit", ".js-group-requirement-add-form", saveForm);
    // Update Group Requirement
    $("#group-requirement-list").on("click", "#js-edit-group-requirement-button", loadForm);
    $("#modal").on("submit", ".js-group-requirement-edit-form", saveForm);
});

//GROUP REQUIREMENT COMMENT (GENERAL)
$('.group-requirement-block').on('submit', '.group-requirement-comment-form', function(event) {
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".group-requirement-comments").html(data.html_group_requirement_comment);
                comment.find(".group-requirement-comment-number").html(data.html_group_requirement_comment_number);
            }
            else {
                current_group.find(".group-requirement-comment-form").html(data.html_group_requirement_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// REQUIREMENT (GENERAL)
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-lg").modal("show");
            },
            success: function (data) {
                $("#modal-lg .modal-content").html(data.html_requirement_form);
                // $('#id_function').djangoSelect2();
                $('#fa-function').djangoSelect2({maximumSelectionLength: 1});
                $('#df-function').djangoSelect2({maximumSelectionLength: 1});
                $('#id_user_characteristic').djangoSelect2();
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#requirement-list").html(data.html_requirement);
                    $("#modal-lg").modal("hide");
                }
                else {
                    $("#modal-lg .modal-content").html(data.html_requirement_form);
                    // $('#id_function').djangoSelect2();
                    $('#fa-function').djangoSelect2({maximumSelectionLength: 1});
                    $('#df-function').djangoSelect2({maximumSelectionLength: 1});
                    $('#id_user_characteristic').djangoSelect2();
                }
            }
        });
        return false;
    };

    // Create Requirement
    $("#requirement-add-button").click(loadForm);
    $("#modal-lg").on("submit", ".js-requirement-add-form", saveForm);

    // Update Requirement
    $("#requirement-list").on("click", "#js-edit-requirement-button", loadForm);
    $("#modal-lg").on("submit", ".js-requirement-edit-form", saveForm);

    // Create FA Requirement
    $("#fa-requirement-add-button").click(loadForm);
    $("#modal-lg").on("submit", ".js-fa-requirement-add-form", saveForm);

    // Update FA Requirement
    $("#requirement-list").on("click", "#js-edit-fa-requirement-button", loadForm);
    $("#modal-lg").on("submit", ".js-fa-requirement-edit-form", saveForm);

    // Create V Requirement
    $("#v-requirement-add-button").click(loadForm);
    $("#modal-lg").on("submit", ".js-v-requirement-add-form", saveForm);

    // Update V Requirement
    $("#requirement-list").on("click", "#js-edit-v-requirement-button", loadForm);
    $("#modal-lg").on("submit", ".js-v-requirement-edit-form", saveForm);

    // Create DF Requirement
    $("#df-requirement-add-button").click(loadForm);
    $("#modal-lg").on("submit", ".js-df-requirement-add-form", saveForm);

    // Update DF Requirement
    $("#requirement-list").on("click", "#js-edit-df-requirement-button", loadForm);
    $("#modal-lg").on("submit", ".js-df-requirement-edit-form", saveForm);
});

// REQUIREMENT COMMENT (GENERAL)
$('.requirement-block').on('submit', '.requirement-comment-form', function(event) {
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".requirement-comments").html(data.html_requirement_comment);
                comment.find(".requirement-comment-number").html(data.html_requirement_comment_number);
            }
            else {
                current_group.find(".requirement-comment-form").html(data.html_requirement_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});

// GROUP REQUIREMENT (FA / DF)
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal").modal("show");
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_group_requirement_form);
                $('#id_task').djangoSelect2();
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#group-requirement-table tbody").html(data.html_group_requirement);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_group_requirement_form);
                    $('#id_task').djangoSelect2();
                }
            }
        });
        return false;
    };
    // Create FA Requirement
    $("#fa-group-requirement-add-button").click(loadForm);
    $("#modal").on("submit", ".js-fa-group-requirement-add-form", saveForm);

    // Create DF Requirement
    $("#df-group-requirement-add-button").click(loadForm);
    $("#modal").on("submit", ".js-df-group-requirement-add-form", saveForm);
});

// SPECIFICATION
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-lg").modal("show");
            },
            success: function (data) {
                $("#modal-lg .modal-content").html(data.html_specification_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#specification-list").html(data.html_specification);
                    $("#specification-top").html(data.html_specification_top);
                    $("#modal-lg").modal("hide");
                }
                else {
                    $("#modal-lg .modal-content").html(data.html_specification_form);

                }
            }
        });
        return false;
    };
    // Create Specification
    $("#specification-add-button").click(loadForm);
    $("#modal-lg").on("submit", ".js-specification-add-form", saveForm);
    // Update Specification
    $("#specification-list").on("click", "#js-edit-specification-button", loadForm);
    $("#modal-lg").on("submit", ".js-specification-edit-form", saveForm);
});

// SPECIFICATION COMMENT
$('.specification-block').on('submit', '.specification-comment-form', function(event) {
    event.preventDefault();
    console.log(event.preventDefault());
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
            var current_group = form.closest('.custom-list-group');
            var comment = form.closest('.custom-list-group-item');
            if (data.form_is_valid) {
                current_group.find(".specification-comments").html(data.html_specification_comment);
                comment.find(".specification-comment-number").html(data.html_specification_comment_number);
            }
            else {
                current_group.find(".specification-comment-form").html(data.html_specification_comment_form);
            }
        }
    });
    form[0].reset();
    return false;
});