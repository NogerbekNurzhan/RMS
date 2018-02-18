import json
from django import forms
from django.forms import TextInput, modelformset_factory, Textarea
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2Widget, Select2MultipleWidget
from .widgets import GroupedModelMultiChoiceField, GroupedModelChoiceField
from django.contrib.auth.models import User
from .models import Member, ROLE_CHOICES, GroupRequirementType, GroupRequirement, Requirement, GroupTask, Task, UserCharacteristic, Function, Comment, Purpose, CreationGoal, ObjectInformation, Specification


class MemberAdminForm(forms.ModelForm):
    """
        Форма добавления нового менеджера проекта.
        Form for adding new project manager.
    """
    class Meta:
        model = Member
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MemberAdminForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = tuple(
            choice for choice in ROLE_CHOICES if choice[0] not in ['developer', 'business_analyst', 'system_analyst'])


class MemberAddForm(forms.ModelForm):
    """
        Форма добавления нового участника проекта.
        For for adding new project member.
    """
    user = forms.ModelChoiceField(widget=Select2Widget(), queryset=User.objects.filter(is_staff=False))
    role = forms.ChoiceField(widget=Select2Widget())

    class Meta:
        model = Member
        exclude = ('project',)

    def __init__(self, *args, **kwargs):
        super(MemberAddForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = _('Select the user')
        self.fields['user'].label = _('User')
        self.fields['role'].label = _('Role')
        self.fields['role'].choices = tuple(choice for choice in ROLE_CHOICES if choice[0] not in ['manager'])


class GroupRequirementTypeForm(forms.ModelForm):
    """
        Form 'Group Requirement Type'
        Форма 'Тип Группы Требований'
    """
    class Meta:
        model = GroupRequirementType
        fields = 'is_visible',

    def __init__(self, *args, **kwargs):
        super(GroupRequirementTypeForm, self).__init__(*args, **kwargs)
        self.label_suffix = ''
        self.fields['is_visible'].label = self.instance.symbol + ': ' + self.instance.name

# Formset 'Group Requirement Type' | FormSet 'Тип Группы Требований'
GroupRequirementTypeFormSet = modelformset_factory(GroupRequirementType, max_num=0, form=GroupRequirementTypeForm)


class GroupTaskForm(forms.ModelForm):
    """
        Form 'Group Task'
        Форма 'Комплекс задач'
    """
    class Meta:
        model = GroupTask
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(GroupTaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'placeholder': _('Name'), 'class': 'form-control'})
        self.fields['name'].required = True
        self.fields['name'].error_messages = {'required': 'This field is required.'}


class TaskForm(forms.ModelForm):
    """
        Form 'Task'
        Форма 'Задача'
    """
    class Meta:
        model = Task
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = TextInput(attrs={'placeholder': _('Name'), 'class': 'form-control'})
        self.fields['name'].required = True
        self.fields['name'].error_messages = {'required': 'This field is required.'}


class FunctionForm(forms.ModelForm):
    """
        Form 'Function'
        Форма 'Функция'
    """
    class Meta:
        model = Function
        fields = ('name',)


class UserCharacteristicForm(forms.ModelForm):
    """
        Form 'User Characteristic'
        Форма 'Характеристика Пользователя'
    """
    class Meta:
        model = UserCharacteristic
        fields = ('user_class', 'user_symbol', 'user_description')

    def __init__(self, *args, **kwargs):
        super(UserCharacteristicForm, self).__init__(*args, **kwargs)
        self.fields['user_class'].widget = TextInput(attrs={'class': 'form-control', 'id': 'user-class'})
        self.fields['user_symbol'].widget = TextInput(attrs={'class': 'form-control', 'id': 'user-symbol'})
        self.fields['user_description'].widget = Textarea(attrs={'class': 'form-control', 'id': 'user-description'})


class CommentForm(forms.ModelForm):
    """
        Form 'Comment'
        Форма 'Комментарий'
    """
    class Meta:
        model = Comment
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = TextInput(attrs={'placeholder': _('Comment Text'), 'class': 'form-control', 'autocomplete': 'off'})
        self.fields['text'].required = True
        self.fields['text'].error_messages = {'required': 'This field is required.'}


class PurposeForm(forms.ModelForm):
    """
        Form 'Purpose'
        Форма 'Назначение системы'
    """
    class Meta:
        model = Purpose
        fields = ('text',)


class CreationGoalForm(forms.ModelForm):
    """
        Form 'Creation Goal'
        Форма 'Цели создания системы'
    """
    class Meta:
        model = CreationGoal
        fields = ('text',)


class ObjectInformationForm(forms.ModelForm):
    """
        Form 'Object Information'
        Форма 'Общая информация об объекте автоматизации'
    """
    class Meta:
        model = ObjectInformation
        fields = ('text',)


class GroupRequirementForm(forms.ModelForm):
    """
        Form 'Group Requirement'
        Форма 'Группа Требований'
    """
    class Meta:
        model = GroupRequirement
        fields = ('name',)
        widgets = {'name': TextInput(attrs={'autocomplete': 'off'}), }


class RequirementForm(forms.ModelForm):
    """
        Form 'Requirement'
        Форма 'Требование'
    """
    function = GroupedModelMultiChoiceField(widget=Select2MultipleWidget, queryset=Function.objects.none(), group_by_field='task')

    class Meta:
        model = Requirement
        fields = ('description', 'function')
        widgets = {'description': TextInput(attrs={'autocomplete': 'off'}), }

    def __init__(self, all_functions, *args, **kwargs):
        super(RequirementForm, self).__init__(*args, **kwargs)
        self.fields['function'].queryset = all_functions
        self.fields['function'].widget.attrs['class'] = "function"


class V_RequirementForm(forms.ModelForm):
    """
        Form 'Requirement' for type [V]
        Форма 'Требование' для типа [V]
    """
    user_characteristic = forms.ModelMultipleChoiceField(required=True, widget=Select2MultipleWidget(), queryset=UserCharacteristic.objects.none())

    class Meta:
        model = Requirement
        fields = ('user_characteristic', 'description',)

    def __init__(self, all_user_characteristics, *args, **kwargs):
        super(V_RequirementForm, self).__init__(*args, **kwargs)
        self.fields['user_characteristic'].queryset = all_user_characteristics


class FA_GroupRequirementForm(forms.ModelForm):
    """
        Form 'Group Requirement' for type [FA]
        Форма 'Группа требований' для типа [FA]
    """
    task = GroupedModelChoiceField(required=True, widget=Select2Widget, queryset=Task.objects.none(), group_by_field='group_task')

    class Meta:
        model = GroupRequirement
        fields = ('task',)

    def __init__(self, all_tasks, *args, **kwargs):
        super(FA_GroupRequirementForm, self).__init__(*args, **kwargs)
        self.fields['task'].empty_label = _('Select the task')
        self.fields['task'].queryset = all_tasks


class FA_RequirementForm(forms.ModelForm):
    """
        Form 'Requirement' for type [FA]
        Форма 'Требование' для типа [FA]
    """
    function = GroupedModelMultiChoiceField(required=True, widget=Select2MultipleWidget(), queryset=Function.objects.none(), group_by_field='task')
    user_characteristic = forms.ModelMultipleChoiceField(required=True, widget=Select2MultipleWidget(), queryset=UserCharacteristic.objects.none())

    class Meta:
        model = Requirement
        fields = ('function', 'user_characteristic')

    def __init__(self, all_functions, all_user_characteristics, *args, **kwargs):
        super(FA_RequirementForm, self).__init__(*args, **kwargs)
        self.fields['function'].queryset = all_functions
        self.fields['function'].widget.attrs = {'id': 'fa-function'}
        self.fields['user_characteristic'].queryset = all_user_characteristics


class DF_GroupRequirementForm(forms.ModelForm):
    """
        Form 'Group Requirement' for type [DF]
        Форма 'Группа Требований' для типа [DF]
    """
    task = GroupedModelChoiceField(required=True, widget=Select2Widget, queryset=Task.objects.none(), group_by_field='group_task')

    class Meta:
        model = GroupRequirement
        fields = ('task',)

    def __init__(self, all_tasks, *args, **kwargs):
        super(DF_GroupRequirementForm, self).__init__(*args, **kwargs)
        self.fields['task'].empty_label = _('Select the task')
        self.fields['task'].queryset = all_tasks


class DF_RequirementForm(forms.ModelForm):
    """
        Form 'Requirement' for type [DF]
        Форма 'Требование' для типа [DF]
    """
    function = GroupedModelMultiChoiceField(required=True, widget=Select2MultipleWidget(), queryset=Function.objects.none(), group_by_field='task')

    class Meta:
        model = Requirement
        fields = ('function',)

    def __init__(self, all_functions, *args, **kwargs):
        super(DF_RequirementForm, self).__init__(*args, **kwargs)
        self.fields['function'].queryset = all_functions
        self.fields['function'].widget.attrs = {'id': 'df-function'}


class RequirementFormTree(forms.ModelForm):
    """
        Древовидная поля для вывода функций: Комплекс задач -> Задачи -> Функции
    """
    class Meta:
        model = Requirement
        fields = 'description', 'function'
        widgets = {
            'function': forms.CheckboxSelectMultiple
        }

    def __init__(self, *args, **kwargs):
        all_functions = kwargs.pop('all_functions', None)
        super(RequirementFormTree, self).__init__(*args, **kwargs)
        if all_functions:
            self.fields['function'].queryset = all_functions
        self.fields['function'].queryset = self.fields['function'].queryset.select_related(
            'task', 'task__group_task')

    def data_tree(self):
        tree = {}
        for f in self.fields['function'].queryset:
            tree.setdefault(
                f.task.group_task.symbol + ": " + f.task.group_task.name, {}
            ).setdefault(
                 f.task.symbol + " " + f.task.name, []
            ).append(str(f.code))
        date_tree_template = "<div class='data-tree' data-tree='{}' data-field='{}'></div>"
        return mark_safe(date_tree_template.format(json.dumps(tree), 'function'))


class SpecificationForm(forms.ModelForm):
    """
        Form 'Specification'
        Форма 'Спецификация'
    """
    class Meta:
        model = Specification
        fields = ('description', )
