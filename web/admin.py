from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from markdownx.admin import MarkdownxModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ProjectModel, Weekly, UserForWeekly


# 个性化设置
admin.site.site_title = '项目管理系统'
admin.site.site_header = '项目管理系统'
admin.site.index_title = '项目管理首页'
admin.site.site_url = None  # 没有site


class MyMixin():
    def save_model(self, request, obj, form, change):
        obj.user = request.user  # 默认设置当前用户为评论者
        # pdb.set_trace()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # 用户只能查看自己的和公开的
        qs = super().get_queryset(request)
        return qs.filter(Q(user=request.user) | Q(public=True))

    def has_change_permission(self, request, obj=None):
        # 用户只能修改自己的，不能修改别人的
        if obj is None:
            return True

        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        # 用户只能删除自己的，不能删除别人的
        if obj is None:
            return True

        return obj.user == request.user


class UserMixin():
    def get_queryset(self, request):
        # 用户只能查看自己的和公开的
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)

    def has_change_permission(self, request, obj=None):
        # 用户只能修改自己的，不能修改别人的
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj == request.user

    def has_delete_permission(self, request, obj=None):
        # 用户只能删除自己的，不能删除别人的
        if obj is None:
            return True
        if request.user.is_superuser:
            return True
        return obj == request.user

class ProjectModelResource(resources.ModelResource):
    class Meta:
        model = ProjectModel


# @admin.register(ProjectModel)
class ProjectModelAdmin(MyMixin, ImportExportModelAdmin):
# class ProjectModelAdmin(MarkdownxModelAdmin):
    resource_classes = [ProjectModelResource]
    list_display = ['name', 'user', 'what',
                    'priority', 'end_date', 'duration', 'status']
    list_filter = ['user', 'status', 'priority', 'end_date']
    search_fields = ['name', 'what', 'why', 'how', 'think']
    ordering = ['status', '-priority', 'end_date']

    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏


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


class UserForWeeklyInline(admin.StackedInline):
    model = UserForWeekly
    can_delete = False
    verbose_name_plural = "employee"


# Define a new User admin
class UserAdmin(UserMixin, BaseUserAdmin):
    inlines = [UserForWeeklyInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# register
admin.site.register(ProjectModel, ProjectModelAdmin)
admin.site.register(Weekly, WeeklyAdmin)
# admin.site.register(UserForWeekly)
