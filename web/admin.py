from django.contrib import admin
from django.db.models import Q
from markdownx.admin import MarkdownxModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ProjectModel


# 个性化设置
admin.site.site_title = '项目管理系统'
admin.site.site_header = '项目管理系统'
admin.site.index_title = '项目管理首页'
admin.site.site_url = None  # 没有site


class ProjectModelResource(resources.ModelResource):
    class Meta:
        model = ProjectModel


# @admin.register(ProjectModel)
# class ProjectModelAdmin(admin.ModelAdmin):
class ProjectModelAdmin(ImportExportModelAdmin):
    resource_classes = [ProjectModelResource]
# class ProjectModelAdmin(MarkdownxModelAdmin):
    list_display = ['name', 'user', 'what',
                    'priority', 'end_date', 'duration', 'status']
    list_filter = ['user', 'status', 'priority', 'end_date']
    search_fields = ['name', 'what', 'why', 'how', 'think']
    ordering = ['status', '-priority', 'end_date']

    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏

    def save_model(self, request, obj, form, change):
        obj.user = request.user  # 默认设置当前用户为评论者
        # pdb.set_trace()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # 用户只能修改自己的ProjectModel和公开的ProjectModel
        return qs.filter(Q(user=request.user) | Q(public=True))

    def has_change_permission(self, request, obj=None):
        # 用户只能修改自己的ProjectModel，不能修改别人的ProjectModel
        if obj is None:
            return True

        return obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        # 用户只能删除自己的ProjectModel，不能删除别人的ProjectModel
        if obj is None:
            return True

        return obj.user == request.user


#
# @admin.register(StepModel)
# class StepModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'status', 'sub_step']
#     list_filter = ['status']
#     search_fields = ['name', 'sub_step']
#     ordering = ['name']


# register
admin.site.register(ProjectModel, ProjectModelAdmin)
