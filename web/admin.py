from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from markdownx.admin import MarkdownxModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ProjectModel, Weekly, UserForWeekly, House, HouseItem


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

"""===============================project================================="""
class ProjectModelResource(resources.ModelResource):
    class Meta:
        model = ProjectModel


# @admin.register(ProjectModel)
class ProjectModelAdmin(MyMixin, ImportExportModelAdmin):
# class ProjectModelAdmin(MarkdownxModelAdmin):
    resource_classes = [ProjectModelResource]
    list_display = ['name', 'user', 'what', 'priority', 'end_date', 'duration', 'status']
    list_filter = ['user', 'status', 'priority', 'end_date']
    search_fields = ['name', 'what', 'why', 'how', 'think']
    ordering = ['status', '-priority', 'end_date']

    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'what', 'status')
        }),
        ('详情信息', {
            'fields': ('why', 'priority', 'public',
                       'start_date', 'end_date', 'how', 'attachments', 'think')
        }),
    )

"""===============================weekly================================="""
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


class UserForWeeklyInline(admin.StackedInline):
    model = UserForWeekly
    can_delete = False
    verbose_name_plural = "employee"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UserForWeeklyInline]




"""===============================house================================="""

class HouseItemInline(admin.TabularInline):
    model = HouseItem
    extra = 1
    fields = ('name', 'price', 'quantity', 'condition')
    # readonly_fields = ('created_at', 'updated_at')


class HouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'status', 'monthly_income')
    list_filter = ('status',)
    search_fields = ('name', 'address')
    
    inlines = [HouseItemInline] # 显示房屋物品的内联表单
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'address', 'status')
        }),
        ('房屋详情', {
            'fields': ('area', 'monthly_expense', 'monthly_rent', 'description')
        }),
    )


class HouseItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'house', 'quantity', 'condition', 'price', 'total_price', 'description')
    list_filter = ('condition', 'house')
    search_fields = ('name', 'house__name')
    
    # fieldsets = (
    #     ('基本信息', {
    #         'fields': ('name', 'house', 'quantity', 'condition',)
    #     }),
    #     ('详情', {
    #         'fields': ('price', 'description')
    #     }),
    # )
    
    
    
    
    
"""===============================register================================="""
    
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
admin.site.register(ProjectModel, ProjectModelAdmin)

admin.site.register(Weekly, WeeklyAdmin)
admin.site.register(UserForWeekly, UserForWeeklyAdmin)

admin.site.register(House, HouseAdmin)
admin.site.register(HouseItem, HouseItemAdmin)
