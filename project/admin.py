from django.contrib import admin

from .models import Project, Member, GroupRequirementTypeDictionary, UserCharacteristicDictionary
from .forms import MemberAdminForm


class MemberInline(admin.TabularInline):
    model = Member
    form = MemberAdminForm
    extra = 1
    max_num = 1

    def get_queryset(self, request):
        queryset = super(MemberInline, self).get_queryset(request)
        return queryset.filter(role='manager')


class MemberAdmin(admin.ModelAdmin):
    inlines = (MemberInline,)
    readonly_fields = ('code',)
    fields = ('name', 'description', 'code', 'status')

admin.site.register(Project, MemberAdmin)
admin.site.register(GroupRequirementTypeDictionary)
admin.site.register(UserCharacteristicDictionary)
