from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
import uuid
import reversion


# Статусы проекта | The status of the project
STATUS_CHOICES = (
    ('open', _('Active')),
    ('close', _('Finished'))
)


# Модель "Проект" | "Project" Model
class Project(models.Model):
    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_('Name'), max_length=250)

    description = models.TextField(_('Description'))

    creation_date = models.DateTimeField(_('Date of creation'), auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    members = models.ManyToManyField(User, through='Member', help_text=_('Members'))

    status = models.CharField(_('Status'), default='open', max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ('-creation_date',)
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project:project_detail', args=[self.code])


# Роли пользователей в проекте | User roles in the project
ROLE_CHOICES = (
    ('manager', _('Manager')),
    ('developer', _('Developer')),
    ('business_analyst', _('Business Analyst')),
    ('system_analyst', _('System Analyst')),
)


# Модель "Участник" | "Member" Model
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    role = models.CharField(_('Role'), max_length=20, choices=ROLE_CHOICES)


# Словать для модели "Характеристики пользователя" | Dictionary for "User Characteristic" model
# Создается администратором системы | Created by system administrator
class UserCharacteristicDictionary(models.Model):
    user_class = models.CharField(_('Class'), max_length=250)

    user_symbol = models.CharField(_('Symbol'), max_length=250)

    user_description = models.TextField(_('Description'))

    def __str__(self):
        return self.user_symbol + ' - ' + self.user_class


# Модель "Характеристика пользователя" | "User Characteristic" Model
@reversion.register()
class UserCharacteristic(models.Model):
    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    user_class = models.CharField(_('Class'), max_length=250)

    user_symbol = models.CharField(_('Symbol'), max_length=250)

    user_description = models.TextField(_('Description'))

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    def __str__(self):
        return self.user_symbol + ' - ' + self.user_class


# Модель "Группа задач" | "Group Task" Model
@reversion.register()
class GroupTask(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_('Name'), max_length=250)

    symbol = models.CharField(_('Symbol'), max_length=250, editable=False)

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    def __str__(self):
        return self.symbol + ': ' + self.name

    def get_absolute_url(self):
        return reverse('project:group_task_detail', args=[self.project_id, self.code])

    class Meta:
        ordering = ('create_time', )


# Модель "Задача" | "Task" Model
@reversion.register()
class Task(models.Model):
    group_task = models.ForeignKey(GroupTask, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(_('Name'), max_length=250)

    symbol = models.CharField(_('Symbol'), max_length=250, editable=False)

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    def __str__(self):
        return self.symbol + ': ' + self.name

    class Meta:
        ordering = ('create_time', )


# Модель "Функция" | "Function" Model
@reversion.register()
class Function(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    symbol = models.CharField(_('Symbol'), max_length=250, editable=False)

    name = models.CharField(_('Name'), max_length=250)

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    def __str__(self):
        return self.symbol + ': ' + self.name

    class Meta:
        ordering = ('create_time', )


# Модель 'Комментарий' | 'Comment' Model
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment Author: {}, Comment Time: {}, Comment Text: {}'.format(self.author, self.created, self.text)


# Назначение системы
@reversion.register()
class Purpose(models.Model):
    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    text = models.TextField(_('Text'))

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)


# Цели создания системы
@reversion.register()
class CreationGoal(models.Model):
    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    text = models.TextField(_('Text'))

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)


# Общие сведения об объекте автоматизации
@reversion.register()
class ObjectInformation(models.Model):
    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    text = models.TextField(_('Text'))

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)


# Словарь для модели "Тип группы требований" | Dictionary for "Group Requirement Type" modal
# Создается администратором системы | Created by system administrator
class GroupRequirementTypeDictionary(models.Model):
    symbol = models.CharField(_('Symbol'), max_length=250)

    name = models.CharField(_('Name'), max_length=250)

    def __str__(self):
        return self.symbol + ' - ' + self.name


# Модель "Тип группы требований" | "Group Requirement Type" Model
class GroupRequirementType(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    symbol = models.CharField(_('Symbol'), max_length=250)

    name = models.CharField(_('Name'), max_length=250)

    is_visible = models.BooleanField(default=False)

    create_time = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('project:group_requirement_type_detail', args=[self.project_id, self.code])

    def __str__(self):
        return self.symbol + ' - ' + self.name


# Модель "Группа требований" | "Group Requirement" Model
@reversion.register()
class GroupRequirement(models.Model):
    group_requirement_type = models.ForeignKey(GroupRequirementType, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    symbol = models.CharField(_('Symbol'), max_length=250)

    name = models.CharField(_('Name'), max_length=250)

    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True)

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    def __str__(self):
        return self.symbol + ' - ' + self.name


# Модель "Требование" | "Requirement" Model
@reversion.register()
class Requirement(models.Model):
    group_requirement = models.ForeignKey(GroupRequirement, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    symbol = models.CharField(_('Symbol'), max_length=250)

    description = models.TextField(_('Description'))

    comments = models.ManyToManyField("Comment")

    function = models.ManyToManyField("Function")

    user_characteristic = models.ManyToManyField('UserCharacteristic')

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)

    def __str__(self):
        return self.symbol + ' - ' + self.description


# Модель "Спецификая" | "Specification" Model
@reversion.register()
class Specification(models.Model):
    requirement = models.ForeignKey(Requirement, on_delete=models.CASCADE)

    code = models.UUIDField(_('Code'), primary_key=True, default=uuid.uuid4, editable=False)

    symbol = models.CharField(_('Symbol'), max_length=250)

    description = models.TextField(_('Description'))

    comments = models.ManyToManyField("Comment")

    create_time = models.DateTimeField(auto_now_add=True)

    revision_date = models.DateTimeField(_('Date of last update'), auto_now=True)
