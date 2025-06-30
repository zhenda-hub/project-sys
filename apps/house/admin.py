from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import House, HouseItem
from apps.core.admin import DefaultMixin


class HouseItemInline(admin.TabularInline):
    model = HouseItem
    extra = 1
    fields = ('name', 'price', 'quantity', 'condition')


class HouseAdmin(DefaultMixin, ImportExportModelAdmin):
    list_display = ('name', 'user', 'address', 'status', 'monthly_income')
    list_filter = ('status', 'user')
    search_fields = ('name', 'address', 'user')
    
    inlines = [HouseItemInline] # 显示房屋物品的内联表单
    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'user', 'address', 'status')
        }),
        ('房屋详情', {
            'fields': ('public', 'area', 'monthly_expense', 'monthly_rent', 'description')
        }),
    )


    def save_formset(self, request, form, formset, change):
        """
        重写 save_formset 方法，处理内联表单的保存逻辑
        """
        # breakpoint()
        if formset.model == HouseItem:
            instances = formset.save(commit=False)
            for instance in instances:
                if not instance.user_id:
                    instance.user = request.user
                instance.save()
            formset.save_m2m()
        else:
            super().save_formset(request, form, formset, change)

class HouseItemAdmin(DefaultMixin, ImportExportModelAdmin):
    list_display = ('name', 'house', 'user', 'quantity', 'condition', 'price', 'total_price', 'description')
    list_filter = ('condition', 'house', 'user')
    search_fields = ('name', 'house__name', 'user')

    readonly_fields = ['user']  # 只读字段，不能编辑，编辑页自动隐藏
    # fieldsets = (
    #     ('基本信息', {
    #         'fields': ('name', 'house', 'quantity', 'condition',)
    #     }),
    #     ('详情', {
    #         'fields': ('price', 'description')
    #     }),
    # )
    
    
admin.site.register(House, HouseAdmin)
admin.site.register(HouseItem, HouseItemAdmin)
