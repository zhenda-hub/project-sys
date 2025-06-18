from django.contrib import admin
from django.db.models import Q
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.core.admin import MyMixin
from .models import ProjectModel

class ProjectModelResource(resources.ModelResource):
    class Meta:
        model = ProjectModel

class ProjectModelAdmin(MyMixin, ImportExportModelAdmin):
    resource_classes = [ProjectModelResource]
    list_display = ['name', 'user', 'what', 'priority', 'end_date', 'duration', 'status']
    list_filter = ['user', 'status', 'priority', 'end_date']
    search_fields = ['name', 'what', 'why', 'how', 'think']
    ordering = ['status', '-priority', 'end_date']

    readonly_fields = ['user']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'what', 'status')
        }),
        ('详情信息', {
            'fields': ('why', 'priority', 'public',
                       'start_date', 'end_date', 'how', 'attachments', 'think')
        }),
    )


admin.site.register(ProjectModel, ProjectModelAdmin)
