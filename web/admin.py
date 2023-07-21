from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import *


# 个性化设置
admin.site.site_title = '项目管理系统'
admin.site.site_header = '项目管理系统'
admin.site.index_title = '项目管理首页'


@admin.register(ProjectModel)
class ProjectModelAdmin(admin.ModelAdmin):
# class ProjectModelAdmin(MarkdownxModelAdmin):
    list_display = ['name', 'what', 'priority', 'end_date', 'duration', 'status']
    list_filter = ['status', 'priority', 'end_date']
    search_fields = ['name', 'what', 'why', 'how', 'think']
    ordering = ['status', '-priority', 'end_date']

    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏

    def save_model(self, request, obj, form, change):
        obj.user = request.user  # 默认设置当前用户为评论者
        # pdb.set_trace()
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

#
# @admin.register(StepModel)
# class StepModelAdmin(admin.ModelAdmin):
#     list_display = ['name', 'status', 'sub_step']
#     list_filter = ['status']
#     search_fields = ['name', 'sub_step']
#     ordering = ['name']