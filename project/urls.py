from django.conf.urls import url

from project.views import (dashboard, project_detail, project_member_add, group_task_add, group_task_edit, group_task_detail, group_task_reversions, group_task_revert, group_task_comment_add, task_add, task_edit, task_detail, task_reversions, task_revert, task_comment_add, function_add, function_edit, function_reversions, function_revert, function_comment_add, user_characteristic_add, user_characteristic_autocomplete, user_characteristic_edit, user_characteristic_reversions, user_characteristic_revert, user_characteristic_comment_add, group_requirement_type_add, group_requirement_type_detail, purpose_add, purpose_edit, purpose_reversions, purpose_revert, purpose_comment_add, creation_goal_add, creation_goal_edit, creation_goal_reversions, creation_goal_revert, creation_goal_comment_add, object_information_add, object_information_edit, object_information_reversions, object_information_revert, object_information_comment_add, group_requirement_add, group_requirement_edit, group_requirement_detail, group_requirement_reversions, group_requirement_revert, group_requirement_comment_add, requirement_add, requirement_edit, requirement_reversions, requirement_revert, requirement_comment_add, requirement_detail, v_requirement_add, v_requirement_edit, fa_group_requirement_add, fa_requirement_add, fa_requirement_edit, df_group_requirement_add, df_requirement_add, df_requirement_edit, specification_add, specification_edit, specification_reversions, specification_revert, specification_comment_add, generate_pdf)

urlpatterns = [
    # Dashboard
    url(r'^$', dashboard, name='dashboard'),

    # PROJECT DETAIL
    url(r'^(?P<project_code>[0-9a-f-]+)/$',
        project_detail,
        name='project_detail'),

    # PROJECT MEMBER ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/add/member/$',
        project_member_add,
        name='project_member_add'),

    # GROUP TASK ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/group_task_add/$',
        group_task_add,
        name='group_task_add'),

    # GROUP TASK EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/group_task_edit/$',
        group_task_edit,
        name='group_task_edit'),

    # GROUP TASK REVERSION
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/group_task_reversions/$',
        group_task_reversions,
        name='group_task_reversions'),

    # GROUP TASK REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<group_task_reversion_id>\d+)/group_task_revert/$',
        group_task_revert,
        name='group_task_revert'),

    # GROUP TASK DETAIL
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/group_task_detail/$',
        group_task_detail,
        name='group_task_detail'),

    # GROUP TASK COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/group_task_comment_add/$',
        group_task_comment_add,
        name='group_task_comment_add'),

    # TASK ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/task_add/$',
        task_add,
        name='task_add'),

    # TASK EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/task_edit/$',
        task_edit,
        name='task_edit'),

    # TASK REVERSION
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/task_reversions/$',
        task_reversions,
        name='task_reversions'),

    # TASK REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/(?P<task_reversion_id>\d+)/task_revert/$',
        task_revert,
        name='task_revert'),

    # TASK DETAIL
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/task_detail/$',
        task_detail,
        name='task_detail'),

    # TASK COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/task_comment_add/$',
        task_comment_add,
        name='task_comment_add'),

    # FUNCTION ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/function_add/$',
        function_add,
        name='function_add'),

    # FUNCTION EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/(?P<function_code>[0-9a-f-]+)/function_edit/$',
        function_edit,
        name='function_edit'),

    # FUNCTION COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/(?P<function_code>[0-9a-f-]+)/function_comment_add/$',
        function_comment_add,
        name='function_comment_add'),

    # FUNCTION REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/(?P<function_code>[0-9a-f-]+)/function_reversions/$',
        function_reversions,
        name='function_reversions'),

    # FUNCTION REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_task_code>[0-9a-f-]+)/(?P<task_code>[0-9a-f-]+)/(?P<function_code>[0-9a-f-]+)/(?P<function_reversion_id>\d+)/function_revert/$',
        function_revert,
        name='function_revert'),

    # USER CHARACTERISTIC ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/user_characteristic_add/$',
        user_characteristic_add,
        name='user_characteristic_add'),

    # USER CHARACTERISTIC AUTOCOMPLETE
    url(r'^user_characteristic_autocomplete/$',
        user_characteristic_autocomplete,
        name='user_characteristic_autocomplete'),

    # USER CHARACTERISTIC EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<user_characteristic_code>[0-9a-f-]+)/user_characteristic_edit/$',
        user_characteristic_edit,
        name='user_characteristic_edit'),

    # USER CHARACTERISTIC REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<user_characteristic_code>[0-9a-f-]+)/user_characteristic_reversions/$',
        user_characteristic_reversions,
        name='user_characteristic_reversions'),

    # USER CHARACTERISTIC REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<user_characteristic_code>[0-9a-f-]+)/(?P<user_characteristic_reversion_id>\d+)/user_characteristic_revert/$',
        user_characteristic_revert,
        name='user_characteristic_revert'),

    # USER CHARACTERISTIC COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<user_characteristic_code>[0-9a-f-]+)/user_characteristic_comment_add/$',
        user_characteristic_comment_add,
        name='user_characteristic_comment_add'),

    # GROUP REQUIREMENT TYPE ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/group_requirement_type_add/$',
        group_requirement_type_add,
        name='group_requirement_type_add'),

    # GROUP REQUIREMENT TYPE DETAIL
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/group_requirement_type_detail/$',
        group_requirement_type_detail,
        name='group_requirement_type_detail'),

    # PURPOSE ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/purpose_add/$',
        purpose_add,
        name='purpose_add'),

    # PURPOSE EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<purpose_code>[0-9a-f-]+)/purpose_edit/$',
        purpose_edit,
        name='purpose_edit'),

    # PURPOSE REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<purpose_code>[0-9a-f-]+)/purpose_reversions/$',
        purpose_reversions,
        name='purpose_reversions'),

    # PURPOSE REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<purpose_code>[0-9a-f-]+)/(?P<purpose_reversion_id>\d+)/purpose_revert/$',
        purpose_revert,
        name='purpose_revert'),

    # PURPOSE COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<purpose_code>[0-9a-f-]+)/purpose_comment_add/$',
        purpose_comment_add,
        name='purpose_comment_add'),

    # CREATION GOAL ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/creation_goal_add/$',
        creation_goal_add,
        name='creation_goal_add'),

    # CREATION GOAL EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<creation_goal_code>[0-9a-f-]+)/creation_goal_edit/$',
        creation_goal_edit,
        name='creation_goal_edit'),

    # CREATION GOAL REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<creation_goal_code>[0-9a-f-]+)/creation_goal_reversions/$',
        creation_goal_reversions,
        name='creation_goal_reversions'),

    # CREATION GOAL REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<creation_goal_code>[0-9a-f-]+)/(?P<creation_goal_reversion_id>\d+)/creation_goal_revert/$',
        creation_goal_revert,
        name='creation_goal_revert'),

    # CREATION GOAL COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<creation_goal_code>[0-9a-f-]+)/creation_goal_comment_add/$',
        creation_goal_comment_add,
        name='creation_goal_comment_add'),

    # OBJECT INFORMATION ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/object_information_add/$',
        object_information_add,
        name='object_information_add'),

    # OBJECT INFORMATION EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<object_information_code>[0-9a-f-]+)/object_information_edit/$',
        object_information_edit,
        name='object_information_edit'),

    # OBJECT INFORMATION REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<object_information_code>[0-9a-f-]+)/object_information_reversions/$',
        object_information_reversions,
        name='object_information_reversions'),

    # OBJECT INFORMATION REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<object_information_code>[0-9a-f-]+)/(?P<object_information_reversion_id>\d+)/object_information_revert/$',
        object_information_revert,
        name='object_information_revert'),

    # OBJECT INFORMATION COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<object_information_code>[0-9a-f-]+)/object_information_comment_add/$',
        object_information_comment_add,
        name='object_information_comment_add'),

    # GROUP REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/group_requirement_add/$',
        group_requirement_add,
        name='group_requirement_add'),

    # GROUP REQUIREMENT EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/group_requirement_edit/$',
        group_requirement_edit,
        name='group_requirement_edit'),

    # GROUP REQUIREMENT REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/group_requirement_reversions/$',
        group_requirement_reversions,
        name='group_requirement_reversions'),

    # GROUP REQUIREMENT REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<group_requirement_reversion_id>\d+)/group_requirement_revert/$',
        group_requirement_revert,
        name='group_requirement_revert'),

    # GROUP REQUIREMENT COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/group_requirement_comment_add/$',
        group_requirement_comment_add,
        name='group_requirement_comment_add'),

    # GROUP REQUIREMENT DETAIL
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/group_requirement_detail/$',
        group_requirement_detail,
        name='group_requirement_detail'),

    # REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/requirement_add/$',
        requirement_add,
        name='requirement_add'),

    # REQUIREMENT EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/requirement_edit/$',
        requirement_edit,
        name='requirement_edit'),

    # REQUIREMENT DETAIL
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/requirement_detail/$',
        requirement_detail,
        name='requirement_detail'),

    # REQUIREMENT REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/requirement_reversions/$',
        requirement_reversions,
        name='requirement_reversions'),

    # REQUIREMENT REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/(?P<requirement_reversion_id>\d+)/requirement_revert/$',
        requirement_revert,
        name='requirement_revert'),

    # REQUIREMENT COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/requirement_comment_add/$',
        requirement_comment_add,
        name='requirement_comment_add'),

    # [V] REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/v_requirement_add/$',
        v_requirement_add,
        name='v_requirement_add'),

    # [V] REQUIREMENT EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/v_requirement_edit/$',
        v_requirement_edit,
        name='v_requirement_edit'),

    # [FA] GROUP REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/fa_group_requirement_add/$',
        fa_group_requirement_add,
        name='fa_group_requirement_add'),

    # [FA] REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/fa_requirement_add/$',
        fa_requirement_add,
        name='fa_requirement_add'),

    # [FA] REQUIREMENT EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/fa_requirement_edit/$',
        fa_requirement_edit,
        name='fa_requirement_edit'),

    # [DF] GROUP REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/df_group_requirement_add/$',
        df_group_requirement_add,
        name='df_group_requirement_add'),

    # [DF] REQUIREMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/df_requirement_add/$',
        df_requirement_add,
        name='df_requirement_add'),

    # [DF] REQUIREMENT EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/df_requirement_edit/$',
        df_requirement_edit,
        name='df_requirement_edit'),

    # SPECIFICATION ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/specification_add/$',
        specification_add,
        name='specification_add'),

    # SPECIFICATION EDIT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/(?P<specification_code>[0-9a-f-]+)/specification_edit/$',
        specification_edit,
        name='specification_edit'),

    # SPECIFICATION REVISIONS
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/(?P<specification_code>[0-9a-f-]+)/specification_reversions/$',
        specification_reversions,
        name='specification_reversions'),

    # SPECIFICATION REVERT
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/(?P<specification_code>[0-9a-f-]+)/(?P<specification_reversion_id>\d+)/specification_revert/$',
        specification_revert,
        name='specification_revert'),

    # SPECIFICATION COMMENT ADD
    url(r'^(?P<project_code>[0-9a-f-]+)/(?P<group_requirement_type_code>[0-9a-f-]+)/(?P<group_requirement_code>[0-9a-f-]+)/(?P<requirement_code>[0-9a-f-]+)/(?P<specification_code>[0-9a-f-]+)/specification_comment_add/$',
        specification_comment_add,
        name='specification_comment_add'),

    # GENERATE_PDF
    url(r'^(?P<project_code>[0-9a-f-]+)/generate_pdf/$',
        generate_pdf,
        name='generate_pdf'),
]
