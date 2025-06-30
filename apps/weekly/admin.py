from django.contrib import admin
from django.http import HttpRequest
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.core.admin import DefaultMixin
from .models import Weekly, UserForWeekly


"""WeeklyAdmin"""
class WeeklyResource(resources.ModelResource):
    class Meta:
        model = Weekly

class WeeklyAdmin(DefaultMixin, ImportExportModelAdmin):
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

    
class UserForWeeklyAdmin(DefaultMixin, ImportExportModelAdmin):
    resource_classes = [UserForWeeklyResource]
    list_display = ['user', 'birthday', 'life']
    list_filter = ['user', 'life']
    search_fields = ['user']
    
    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏


admin.site.register(Weekly, WeeklyAdmin)
admin.site.register(UserForWeekly, UserForWeeklyAdmin)
