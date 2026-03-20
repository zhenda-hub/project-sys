from django.contrib import admin
from django.db.models import Q
from django.urls import path
from django.shortcuts import render
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.core.admin import DefaultMixin
from .models import ProjectModel

class ProjectModelResource(resources.ModelResource):
    class Meta:
        model = ProjectModel

class ProjectModelAdmin(DefaultMixin, ImportExportModelAdmin):
    resource_classes = [ProjectModelResource]
    list_display = ['name', 'user', 'what', 'priority', 'end_date', 'duration', 'status']
    list_filter = ['user', 'status', 'priority', 'end_date']
    search_fields = ['name', 'what', 'why', 'how', 'think']
    ordering = ['status', '-priority', 'end_date']
    import_export_change_list_template = "admin/projects/change_list_import_export.html"

    readonly_fields = ['user']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'what', 'status')
        }),
        ('详情信息', {
            'fields': ('why', 'priority', 'public',
                       'start_date', 'end_date', 'how', 'attachments', 'think')
        }),
        # ('CKEditor4 测试', {
        #     'fields': ('ck4_test',)
        # }),
    )

    def get_urls(self):
        """添加自定义甘特图视图 URL"""
        urls = super().get_urls()
        custom_urls = [
            path('gantt/', self.admin_site.admin_view(self.gantt_view),
                 name='projects_projectmodel_gantt'),
        ]
        return custom_urls + urls

    def gantt_view(self, request):
        """甘特图页面视图 - 支持列表页过滤器参数"""
        # Django admin 内部参数（不应传递给 filter）
        ADMIN_INTERNAL_PARAMS = ('all', 'o', 'p', 'q', '_popup', '_to_field')

        # 获取基础 queryset（权限过滤）
        if request.user.is_superuser:
            projects = ProjectModel.objects.all()
        else:
            projects = ProjectModel.objects.filter(
                Q(user=request.user) | Q(public=True)
            )

        # 应用列表页过滤器参数（排除 admin 内部参数）
        filter_params = {
            k: v for k, v in request.GET.items()
            if k not in ADMIN_INTERNAL_PARAMS
        }
        if filter_params:
            projects = projects.filter(**filter_params)

        # 按结束时间排序（甘特图原有逻辑）
        projects = sorted(projects, key=lambda p: p.end_date, reverse=True)

        context = {
            **self.admin_site.each_context(request),
            'title': '项目甘特图',
            'projects': projects,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request),
        }
        return render(request, 'admin/projects/gantt.html', context)


admin.site.register(ProjectModel, ProjectModelAdmin)
