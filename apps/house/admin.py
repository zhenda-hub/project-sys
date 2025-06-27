from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import House, HouseItem
from apps.core.admin import PublicMixin


# TODO: user public

class HouseItemInline(admin.TabularInline):
    model = HouseItem
    extra = 1
    fields = ('name', 'price', 'quantity', 'condition')


class HouseAdmin(PublicMixin, admin.ModelAdmin):
    list_display = ('name',  'user', 'address', 'status', 'monthly_income')
    list_filter = ('status', 'user',)
    search_fields = ('name', 'address', 'user')
    
    inlines = [HouseItemInline] # 显示房屋物品的内联表单
    readonly_fields = ['user']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'address', 'status')
        }),
        ('房屋详情', {
            'fields': ('public', 'area', 'monthly_expense', 'monthly_rent', 'description')
        }),
    )

class HouseItemAdmin(PublicMixin, admin.ModelAdmin):
    list_display = ('name', 'house', 'quantity', 'condition', 'price', 'total_price', 'description')
    list_filter = ('condition', 'house',)
    search_fields = ('name', 'house__name',)

    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'house', 'quantity', 'condition',)
        }),
        ('详情', {
            'fields': ('public', 'price', 'description')
        }),
    )
    
    
admin.site.register(House, HouseAdmin)
admin.site.register(HouseItem, HouseItemAdmin)
