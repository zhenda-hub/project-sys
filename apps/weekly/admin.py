from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.core.admin import MyMixin
from .models import Weekly, UserForWeekly


"""WeeklyAdmin"""
class WeeklyResource(resources.ModelResource):
    class Meta:
        model = Weekly

class WeeklyAdmin(MyMixin, ImportExportModelAdmin):
    resource_classes = [WeeklyResource]
    list_display = ['date', 'user', 'time_left']
    list_filter = ['date', 'user']
    search_fields = ['date', 'user']
    ordering = ['-date']
    
    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏


"""UserForWeeklyAdmin"""
class UserForWeeklyResource(resources.ModelResource):
    class Meta:
        model = UserForWeekly


class UserForWeeklyMixin():
    def get_queryset(self, request):
        # 用户只能查看自己的和公开的
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        # 用户只能修改自己的，不能修改别人的
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        # 用户只能删除自己的，不能删除别人的
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj.user == request.user
    
    
class UserForWeeklyAdmin(UserForWeeklyMixin, ImportExportModelAdmin):
    resource_classes = [UserForWeeklyResource]
    list_display = ['user', 'birthday', 'life']
    list_filter = ['user', 'life']
    search_fields = ['user']
    
    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏




"""Re-register UserAdmin with the inline"""
class UserForWeeklyInline(admin.StackedInline):
    model = UserForWeekly
    can_delete = False
    verbose_name_plural = "employee"

class UserAdmin(BaseUserAdmin):
    inlines = [UserForWeeklyInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)




admin.site.register(Weekly, WeeklyAdmin)
admin.site.register(UserForWeekly, UserForWeeklyAdmin)
